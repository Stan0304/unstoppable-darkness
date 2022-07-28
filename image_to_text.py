import requests

def detect_text_uri(uri, retry=0, msg=''):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    if retry > 3:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(msg))

    r = requests.get('https://cdn.discordapp.com/attachments/988510802506022975/989190078205157506/unknown.png')
    if r.status_code != 200 and retry > 3:
        raise r.exceptions.HTTPError
    
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=r.content)
    #image = vision.Image()
    #image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    results = []
    for n in range(1,len(texts)):
        text = texts[n]

        vertices = (['{},{}'.format(vertex.x, vertex.y)
            for vertex in text.bounding_poly.vertices])

        results.append({
            'text': '{}'.format(text.description),
            'b0.x': b_round(text.bounding_poly.vertices[0].x),
            'b0.y': b_round(text.bounding_poly.vertices[0].y),
            'b1.x': b_round(text.bounding_poly.vertices[1].x),
            'b1.y': b_round(text.bounding_poly.vertices[1].y),
            'b2.x': b_round(text.bounding_poly.vertices[2].x),
            'b2.y': b_round(text.bounding_poly.vertices[2].y),
            'b3.x': b_round(text.bounding_poly.vertices[3].x),
            'b3.y': b_round(text.bounding_poly.vertices[3].y)
        })
    
    results.sort(key= lambda x: x.get('b3.x'))
    results.sort(key= lambda x: x.get('b3.y'))

    if response.error.message:
        retry+=1
        return detect_text_uri(uri, retry, response.error.message)

    return results

def b_round(x, base=10):
    return base * round((int(x)+1)/base)