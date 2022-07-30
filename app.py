from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_file
import os
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from main import pie_chart, histo_split, histo_split_stacked, show_stories_from_video, individual_info_from_video, getListOfVideosIn

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("completedataset.html") 
@app.route("/<split>")
def rendersplitlink(split): 
    if split == "total": 
        return redirect(url_for('main')) 
    else: 
        selected_list = getListOfVideosIn(split)
        return render_template("splitdataset.html", 
                                split = split, 
                                video_ids_list = selected_list)

""" PLOT FOR COMPLETE DATASET PAGE """
@app.route('/plot_pie_chart.png')
def plot_pie_chart(): 
    fig = pie_chart()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_histo_<split>.png')
def plot_histo(split):
    fig = histo_split(split)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_stacked.png')
def plot_histo_stacked():
    fig = histo_split_stacked()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

""" FUNCTIONS FOR SPLIT DATASET PAGE """

@app.route('/<split>/<selected_video>')
def rendersplitlinkwithvideo(split, selected_video): 
    selected_list = getListOfVideosIn(split)
    nb_of_stories, nb_of_threads = individual_info_from_video(selected_video)
    return render_template("splitdataset.html", 
                            split = split, 
                            video_ids_list = selected_list, 
                            selected_video = selected_video, 
                            nb_of_stories = nb_of_stories, 
                            nb_of_threads = nb_of_threads)

@app.route('/<split>/selected_video_story', methods = ['POST', 'GET'])
def showSelectedVideo(split):
    if request.method == 'GET':
      video_id_selected = request.args.get('video_id_sl')
    else: 
      video_id_selected = request.form['video_id_sl']

    if video_id_selected == 'Choose the video ID': 
        return ('', 204)
    else: 
        return redirect(url_for('rendersplitlinkwithvideo', 
                                split = split, 
                                selected_video = video_id_selected))

@app.route('/plot_timeline_<selectedvideo>.png')
def plot_stories(selectedvideo):
    fig = show_stories_from_video(selectedvideo)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run()