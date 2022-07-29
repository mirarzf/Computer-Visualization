from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_file
import os
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from main import histo_split, show_stories_from_video, show_timeline

app = Flask(__name__)

# @app.route("/", methods=['GET', 'POST'])
# def selected_list(split): 
#     optionslist = 
selected_list = ["P37_102", "P01_09"]

@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("completedataset.html") 
                        #    video_ids_list = selected_list, 
                        #    videoidselected = "P01_09")

@app.route("/<split>")
def rendersplitlink(split): 
    if split == "total": 
        return redirect(url_for('main'))  
    else: 
        # urlofnextpage = split + ".html"
        return render_template("splitdataset.html", 
                                split = split)










@app.route('/plot_histo_<split>.png')
def plot_histo(split):
    fig = histo_split(split)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot_stories.png')
def plot_stories():
    fig = show_stories_from_video()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# @app.route('/selectlist', methods = ['POST', 'GET'])
# def login():
#     if request.method == 'GET':
#       video_id_selected = request.args.get('video_id_sl')
#       return redirect(url_for('success', name = video_id_selected))
#     else: 
#       video_id_selected = request.form['video_id_sl']
#       return redirect(url_for('success', name = video_id_selected))

# @app.route('/plot_timeline_videoidselected.png')
def success(videoidselected):
    fig = show_stories_from_video(videoidselected)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/<split>/selected_video_story/<videoidselected>', methods = ['POST', 'GET'])
def main_selected_vid_iframe(split, videoidselected): 
    show_stories_from_video()
    return render_template("selected_video_story.html", 
                            split = split, 
                            videoidselected = videoidselected)

@app.route('/selectlist', methods = ['POST', 'GET'])
def showSelectedVideo():
    if request.method == 'GET':
      video_id_selected = request.args.get('video_id_sl')
    else: 
      video_id_selected = request.form['video_id_sl']

    # success(videoidselected = video_id_selected)
    show_stories_from_video(video_name = video_id_selected)
    send_file(os.path.join("static", "plot_timeline_videoidselected.png"))
    # return ('', 204)
    return redirect(url_for('main_selected_video_story', videoidselected = video_id_selected))


if __name__ == "__main__":
    app.run()