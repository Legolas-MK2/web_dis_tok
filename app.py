from flask import Flask, render_template, redirect, request
import requests


app = Flask(__name__)

with open('meme.txt', 'r') as f:
    image_urls = [line.strip() for line in f.readlines()]


# Index route
@app.route('/')
def index():
    # Get the current image or video index from the query parameter
    idx = request.args.get('idx', default=0, type=int)

    # Check if the URL is online
    try:
        print(image_urls[idx])
        response = requests.head(image_urls[idx])
        if response.status_code == 200:
            url = image_urls[idx]

            # Check the file extension to determine whether it's an image or a video
            if url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png'):
                # It's an image, use the img HTML tag
                return render_template('index.html', url=url, is_video=False, idx=idx)
            elif url.endswith('.mp4') or url.endswith('.avi') or url.endswith('.mov'):
                # It's a video, use the video HTML tag
                return render_template('index.html', url=url, is_video=True, idx=idx)

    except:
        pass

    # If the current URL is not online, move to the next image
    return redirect('/next?idx=' + str(idx))


# Next route
@app.route('/next')
def next():
    # Get the current image or video index from the query parameter
    idx = request.args.get('idx', default=0, type=int)
    while True:
        print(idx)
        print(image_urls[idx])
        print()
        # Increment the index (with wraparound)
        idx = (idx + 1) % len(image_urls)
        try:
            response = requests.head(image_urls[idx])
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass

    # Redirect to the index route with the updated index
    return redirect('/?idx=' + str(idx))


if __name__ == '__main__':

    app.run(debug=True)


