# app/home/views.py

from flask import abort,render_template,flash,redirect,url_for
from flask_login import current_user,login_required
from .forms import TaskForm
from . import home
from .. import db
from ..models import Task,Employee



@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
def dashboard():
    """
    return the dashboard template on /dashboard route

    """
    return render_template('home/dashboard.html')


@home.route('/dashboardshowall/')
@login_required
def dashboard_showall():
    """
    Render the dashboard show all  template
    """
    tasks = Task.query.filter_by(towhom=Employee.username)
    return render_template('home/taskshowall/dashboard_showall.html',
                           tasks=tasks, title="Tasks")

# @home.route('/dashboardshowtask/<int:id>')
# @login_required
# def showtask(id):
#     """
#
#     to show tasks (all the tasks)
#     """
#
#     tasks = Task.query.filter_by(id=id)
#     return render_template('home/taskshowall/dashboard_showtask.html',tasks=tasks,title="tasks")
@home.route('/dashboardshowtasku/<towhom>')
@login_required
def showtaskparticular(towhom):
    """

    to show tasks (all the tasks)
    """

    tasks = Task.query.filter_by(towhom=towhom)
    return render_template('home/taskshowall/dashboard_showtask.html',tasks=tasks,title="tasks")

@home.route('/dashboardchangestatus/<int:id>', methods=['GET', 'POST'])
@login_required
def changestatus(id):
    """

    to change the status of the task
    """

    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():

        task.description = form.description.data
        task.status = form.status.data


        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the taskshowall page
        return redirect(url_for('home.dashboard_showall'))

    form.description.data = task.description

    form.status.data = task.status


    return render_template('home/taskshowall/dashboard_changestatus.html',form=form,
                           task=task, title="Edit Task")


# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

# add manager dashboard view
@home.route('/taskmanager/dashboard')
@login_required
def manager_dashboard():
    # prevent non-managers from accessing the page
    if not current_user.is_manager:
        abort(403)

    return render_template('home/manager_dashboard.html', title="Dashboard")

