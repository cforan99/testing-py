"""Flask site for Balloonicorn's Party."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


def is_mel(name, email):
    """Is this user Mel?
 
        >>> is_mel('Mel Melitpolski', 'mel@ubermelon.com')
        True
    
        >>> is_mel('Judith Butler', 'judith@awesome.com')
        False

        >>> is_mel('Mel Melitpolski', 'mel@gmail.com')
        True

        >>> is_mel('Not Mel', 'mel@ubermelon.com')
        True

        >>> is_mel('Not Mel', 'mel@gmail.com')
        False
    
    """

    return name == "Mel Melitpolski" or email == "mel@ubermelon.com"



def most_and_least_common_type(treats):
    """Given list of treats, return {most, least} common types.

        Here is a typical case:

        >>> treats = [{'type': 'dessert'}, {'type': 'drink'}, {'type': 'dessert'}]
        >>> most_and_least_common_type(treats)
        ('dessert', 'drink')

        Here is the edge case for one type of food:

        >>> one_treat = [{'type': 'entree'}]
        >>> most_and_least_common_type(one_treat)
        ('entree', 'entree')

        Here is an edge case when there is a tie for most and/or least:

        >>> treats = [{'type': 'dessert'}, {'type': 'drink'}, {'type': 'dessert'}, {'type': 'drink'}]
        >>> most_and_least_common_type(treats)
        ('dessert', 'dessert')

        >>> treats = [{'type': 'dessert'}, {'type': 'drink'}, {'type': 'dessert'}, {'type': 'drink'}, {'type': 'entree'}]
        >>> most_and_least_common_type(treats)
        ('dessert', 'entree')

        >>> treats = [{'type': 'dessert'}, {'type': 'drink'}, {'type': 'dessert'}, {'type': 'drink'}, {'type': 'entree'}, {'type': 'side'}]
        >>> most_and_least_common_type(treats)
        ('dessert', 'side')

        Here is an edge case when there is an empty list:
        >>> empty_list = []
        >>> most_and_least_common_type(empty_list)
        (None, None)


    """ 

    types = {}

    # Count number of each type
    for treat in treats:
        types[treat['type']] = types.get(treat['type'], 0) + 1

    most_count = most_type = None
    least_count = least_type = None

    # Find most, least common
    for ttype, count in types.items():
        if most_count is None or count > most_count:
            most_count = count
            most_type = ttype
        if least_count is None or count < least_count:
            least_count = count
            least_type = ttype

    return (most_type, least_type)


def get_treats():
    """Get treats being brought to the party.

    One day, I'll move this into a database! -- Balloonicorn
    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Heather'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Cynthia'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'David'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Kari'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Denise'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Lavinia'}
    ]


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/treats")
def show_treats():
    """Show treats people are bringing."""

    treats = get_treats()

    most, least = most_and_least_common_type(get_treats())

    return render_template("treats.html",
                           treats=treats,
                           most=most,
                           least=least)


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    if not is_mel(name, email):
        session['rsvp'] = True
        flash("Yay!")
        return redirect("/")

    else:
        flash("Sorry, Mel. This is kind of awkward.")
        return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run()
