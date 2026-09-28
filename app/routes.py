from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.gemini_flash_generator import (
    generate_nutrition_tip_with_flash,
)
from app.gemini_generator import (
    generate_workout_gemini,
)
from app.models import Plan
from app.models import User
from app.schemas import UserInput
from app.updated_plan import (
    update_workout_plan,
)


router = APIRouter()


def render(
    request: Request,
    template: str,
    context: dict,
):

    from app.main import templates

    return templates.TemplateResponse(
        request=request,
        name=template,
        context=context,
    )


@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):

    return render(
        request,
        "index.html",
        {},
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse,
)
def generate_workout(

    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db),
):

    try:

        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

    except Exception as exc:

        return render(
            request,
            "index.html",
            {
                "error": str(exc)
            },
        )


    user = db.scalar(
        select(User).where(
            User.user_id == data.user_id
        )
    )


    if user is None:

        user = User(

            user_id=data.user_id,

            username=data.username,

            age=data.age,

            weight=data.weight,

            goal=data.goal,

            intensity=data.intensity,
        )

        db.add(user)

    else:

        user.username = data.username

        user.age = data.age

        user.weight = data.weight

        user.goal = data.goal

        user.intensity = data.intensity


    workout_plan = generate_workout_gemini(

        data.username,

        data.age,

        data.weight,

        data.goal,

        data.intensity,
    )


    nutrition_tip = (
        generate_nutrition_tip_with_flash(
            data.goal,
            data.age,
        )
    )


    existing_plan = db.scalar(

        select(Plan)

        .where(
            Plan.user_id == data.user_id
        )

        .order_by(
            Plan.id.desc()
        )
    )


    if existing_plan:

        existing_plan.original_plan = (
            workout_plan
        )

        existing_plan.updated_plan = None

        existing_plan.feedback = None

        existing_plan.nutrition_tip = (
            nutrition_tip
        )

    else:

        db.add(

            Plan(

                user_id=data.user_id,

                original_plan=workout_plan,

                nutrition_tip=nutrition_tip,
            )
        )


    db.commit()


    return render(

        request,

        "result.html",

        {

            "user": user,

            "plan": workout_plan,

            "nutrition_tip": nutrition_tip,

            "message": None,
        },
    )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse,
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db),
):

    user = db.scalar(

        select(User).where(
            User.user_id == user_id
        )
    )


    plan = db.scalar(

        select(Plan)

        .where(
            Plan.user_id == user_id
        )

        .order_by(
            Plan.id.desc()
        )
    )


    if user is None or plan is None:

        return render(

            request,

            "index.html",

            {

                "error":
                    "User or workout plan was "
                    "not found. Generate a plan first."
            },
        )


    feedback = feedback.strip()


    if len(feedback) < 3:

        return render(

            request,

            "result.html",

            {

                "user": user,

                "plan":
                    plan.updated_plan
                    or plan.original_plan,

                "nutrition_tip":
                    plan.nutrition_tip,

                "message":
                    "Please enter a little more "
                    "detail in your feedback.",
            },
        )


    revised = update_workout_plan(

        original_plan=plan.original_plan,

        feedback=feedback,

        goal=user.goal,

        intensity=user.intensity,

        age=user.age,
    )


    plan.updated_plan = revised

    plan.feedback = feedback


    db.commit()


    return render(

        request,

        "result.html",

        {

            "user": user,

            "plan": revised,

            "nutrition_tip":
                plan.nutrition_tip,

            "message":
                "Your plan was updated "
                "using your feedback.",
        },
    )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse,
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db),
):

    users = db.scalars(

        select(User)

        .order_by(
            User.created_at.desc()
        )
    ).all()


    rows = []


    for user in users:

        plan = db.scalar(

            select(Plan)

            .where(
                Plan.user_id == user.user_id
            )

            .order_by(
                Plan.id.desc()
            )
        )


        rows.append(

            {
                "user": user,
                "plan": plan,
            }
        )


    return render(

        request,

        "all_users.html",

        {
            "rows": rows
        },
    )


@router.post(
    "/delete-user/{user_id}"
)
def delete_user(

    user_id: str,

    db: Session = Depends(get_db),
):

    user = db.scalar(

        select(User).where(
            User.user_id == user_id
        )
    )


    if user:

        db.delete(user)

        db.commit()


    return RedirectResponse(

        url="/view-all-users",

        status_code=303,
    )


@router.get("/health")
def health():

    return {

        "status": "ok",

        "service": "FitBuddy",
    }