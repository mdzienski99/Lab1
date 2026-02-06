from flask import Flask, request, jsonify, render_template
from analyze import read_image

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/ 
# API at /api/v1/analysis/
@app.route("/api/v1/analysis/", methods=["GET"])
def analysis():
    # Try to get the URI from the JSON
    try:
        get_json = request.get_json(force=True, silent=False)
        image_uri = get_json.get("uri")
        if not image_uri:
            return jsonify({"error": "Missing URI in JSON"}), 400
    except Exception as e:
        return jsonify({
            "error": "Invalid or unreadable JSON",
            "details": str(e)
        }), 400

    # Try to get the text from the image
    try:
        res = read_image(image_uri)

        response_data = {
            "text": res,
            "uri": image_uri
        }

        return jsonify(response_data), 200

    except Exception as e:
        import traceback
        traceback.print_exc()  # <-- shows full error in your Flask terminal

        return jsonify({
            "error": "Error in processing",
            "details": str(e)
        }), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)