from flask import Blueprint, request
from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """
    search_id = args.get("id")
    search_name = args.get("name")
    search_age = args.get("age")
    search_occupation = args.get("occupation")

    results = []

    if search_id:
        user_with_id = next((user for user in USERS if user["id"] == search_id), None)
        if user_with_id:
            results.append(user_with_id)

    if search_name:
        search_name_lower = search_name.lower()
        results.extend([user for user in USERS if search_name_lower in user["name"].lower()])

    if search_age:
        age_lower = int(search_age) - 1
        age_upper = int(search_age) + 1
        results.extend([user for user in USERS if age_lower <= user["age"] <= age_upper])

    if search_occupation:
        search_occupation_lower = search_occupation.lower()
        results.extend([user for user in USERS if search_occupation_lower in user["occupation"].lower()])

    # If no matching search, return all users
    if not results:
        return USERS

    # Remove duplicates from the results
    unique_results = [dict(t) for t in {tuple(d.items()) for d in results}]

    unique_results.sort(
    key=lambda user: (
        -(search_id == user.get("id")) if search_id else 0,
        -(search_name_lower in user.get("name", "").lower()) if search_name else 0,
        -(search_age and (age_lower <= user.get("age", 0) <= age_upper) if user.get("age") else False) if search_age else 0,
        -(search_occupation_lower in user.get("occupation", "").lower()) if search_occupation else 0,
        user.get("id", ""),  # Sorting by id in ascending order
        user.get("name", "").lower(),  # Sorting by name in ascending order
        -user.get("age", 0),  # Sorting by age in descending order
        user.get("occupation", "").lower(),  # Sorting by occupation in ascending order
    ),
)
    return unique_results