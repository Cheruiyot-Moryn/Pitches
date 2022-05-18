from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . forms import PitchForm, CommentForm, CategoryForm
from .import main
from .. import db
from ..models import User, Pitch, Comment, Votes

#display categories on the landing page
@main.route('/')
def index():
    """
    Function that returns index page
    """

    all_pitches = Pitch.query.order_by('id').all()
    print(all_pitches)

    title = 'min1-Pitches'
    return render_template('index.html', title = title, all_pitches=all_pitches)

#Route for adding a new pitch
@main.route('/pitch/newpitch',methods= ['POST','GET'])
@login_required
def new_pitch():
    pitch = PitchForm()
    if pitch.validate_on_submit():
        title = pitch.pitch_title.data
        category = pitch.pitch_category.data
        user_id = current_user

        #update pitch instance

        newPitch = Pitch(pitch_title = title,pitch_category = category,user= user_id)

        #save pitch
        newPitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'NEW PITCH'

    return render_template('pitch.html',title = title, pitchform = pitch)  



# @main.route('/categories/<int:id>')
# def category(id):
#     category = PitchCategory.query.get(id)
#     if category is None:
#         abort(404)
        
#     pitches=Pitch.get_pitches(id)
#     return render_template('category.html', pitches=pitches, category=category)


# @main.route('/add/category', methods=['GET','POST'])
# @login_required
# def new_category():
#     """
#     View new group route function that returns a page with a form to create a category
#     """
    
#     form = CategoryForm()

#     if form.validate_on_submit():
#         name = form.name.data
#         new_category = PitchCategory(name = name)
#         new_category.save_category()

#         return redirect(url_for('.index'))

#     title = 'New category'
#     return render_template('new_category.html', category_form = form, title = title)

@main.route('/category/life',methods= ['GET'])
def displayLifeCategory():
    lifePitches = Pitch.get_pitches('life')
    return render_template('life.html',lifePitches = lifePitches)

@main.route('/category/code',methods= ['POST','GET'])
def displayCodeCategory():
    codePitches = Pitch.get_pitches('code')
    return render_template('code.html',codePitches = codePitches)

@main.route('/category/promotion',methods= ['POST','GET'])
def displayPromotionCategory():
    promotionPitches = Pitch.get_pitches('promotion')
    return render_template('promotion.html',promotionPitches = promotionPitches)

@main.route('/category/pickup',methods= ['POST','GET'])
def displayPickupCategory():
    pickupPitches = Pitch.get_pitches('pickup')
    return render_template('pickup.html',pickupPitches = pickupPitches)


    #view single pitch alongside its comments
@main.route('/comment/<int:id>',methods= ['POST','GET'])
@login_required
def viewPitch(id):
    onepitch = Pitch.getPitchId(id)
    comments = Comment.get_comments(id)

    if request.args.get("like"):
        onepitch.likes = onepitch.likes + 1

        db.session.add(onepitch)
        db.session.commit()

        return redirect("/comment/{pitch_id}".format(pitch_id= id))

    elif request.args.get("dislike"):
        onepitch.dislikes = onepitch.dislikes + 1

        db.session.add(onepitch)
        db.session.commit()

        return redirect("/comment/{pitch_id}".format(pitch_id= id))

    commentForm = CommentForm()
    if commentForm.validate_on_submit():
        opinion = commentForm.opinion.data

        newComment = Comment(opinion = opinion,user = current_user,pitches_id= id)

        newComment.save_comment()

    return render_template('comment.html',commentForm = commentForm,comments = comments,pitch = onepitch)

#adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    """ 
    Function to post comments 
    """
    
    form = CommentForm()
    title = 'Post A Comment'
    pitches = Pitch.query.filter_by(id=id).first()

    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comment(opinion = opinion, user_id = current_user.id, pitches_id = pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id = pitches.id))

    return render_template('comment.html', comment_form = form, title = title)

#Routes upvoting/downvoting pitches
@main.route('/pitch/upvote/<int:id>&<int:vote_type>')
@login_required
def upvote(id,vote_type):
    """
    View function that adds one to the vote_number column in the votes table
    """
    # Query for user
    votes = Votes.query.filter_by(user_id=current_user.id).all()
    print(f'The new vote is {votes}')
    to_str=f'{vote_type}:{current_user.id}:{id}'
    print(f'The current vote is {to_str}')

    if not votes:
        new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
        new_vote.save_vote()
        # print(len(count_likes))
        print('You have a new vote')

    for vote in votes:
        if f'{vote}' == to_str:
            print('You can only vote once')
            break
        else:   
            new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
            new_vote.save_vote()
            print('You have voted')
            break
    # count_likes = Votes.query.filter_by(pitches_id=id, vote=1).all()
    # upvotes=len(count_likes)
    # count_dislikes = Votes.query.filter_by(pitches_id=id, vote=2).all()

    return redirect(url_for('comment.html', id=id))
