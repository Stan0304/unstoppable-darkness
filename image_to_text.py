
def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    result = []
    for n in range(1,len(texts)):
        text = texts[n]
        result.append('text:{}'.format(text.description))

        vertices = (['{},{}'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        result.append('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return result
