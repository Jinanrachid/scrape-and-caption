from flask import Flask, request, jsonify
from claude_model import generate_caption

app = Flask(__name__)

@app.route("/caption", methods=["POST"])
def create_caption():
    '''Endpoint to generate image caption using Claude model.'''
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        image_file = request.files["image"]
        # Convert FileStorage to PIL Image
        caption_text = generate_caption(image_file)
        return jsonify({"caption": caption_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)


