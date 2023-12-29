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
    # Extract search parameters from the args dictionary
    search_id = args.get("id")
    search_name = args.get("name")
    search_age = args.get("age")
    search_occupation = args.get("occupation")

    # Initialize an empty list to store the results
    results = []

    # If the id is provided, include the user with that id in the results
    if search_id:
        user_with_id = next((user for user in USERS if user["id"] == search_id), None)
        if user_with_id:
            results.append(user_with_id)

    # Filter users based on name (case-insensitive partial match)
    if search_name:
        search_name_lower = search_name.lower()
        results.extend([user for user in USERS if search_name_lower in user["name"].lower()])

    # Filter users based on age (within the range of age - 1 to age + 1)
    if search_age:
        age_lower = int(search_age) - 1
        age_upper = int(search_age) + 1
        results.extend([user for user in USERS if age_lower <= user["age"] <= age_upper])

    # Filter users based on occupation (case-insensitive partial match)
    if search_occupation:
        search_occupation_lower = search_occupation.lower()
        results.extend([user for user in USERS if search_occupation_lower in user["occupation"].lower()])

    # If no matching results are found, return all users
    if not results:
        return USERS

    # Remove duplicates from the results
    unique_results = [dict(t) for t in {tuple(d.items()) for d in results}]

    # Sort the results based on the priority of matching criteria
    unique_results.sort(
        key=lambda user: (
            search_id and user.get("id") == search_id,
            search_name and search_name_lower in user.get("name", "").lower(),
            search_age and (age_lower <= user.get("age", 0) <= age_upper if user.get("age") else False),
            search_occupation and search_occupation_lower in user.get("occupation", "").lower(),
        ),
        reverse=True,
    )
    
    return unique_results