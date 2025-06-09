from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/process', methods=['POST'])
def process():
    data = request.json
    url = data.get('url')
    quality = data.get('quality', 'best')

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    video_info = {
        'id': info.get('id'),
        'title': info.get('title'),
        'uploader': info.get('uploader'),
        'duration': info.get('duration'),
        'view_count': info.get('view_count'),
        'thumbnail': info.get('thumbnail'),
    }

    formats = info.get('formats', [])
    download_links = []
    for f in formats:
        if f.get('format_note') == quality or quality == 'best':
            download_links.append({
                'url': f.get('url'),
                'format_id': f.get('format_id'),
                'ext': f.get('ext'),
                'quality': f.get('format_note'),
                'filesize': f.get('filesize'),
                'width': f.get('width'),
                'height': f.get('height'),
                'fps': f.get('fps'),
            })

    return jsonify({
        'success': True,
        'video_info': video_info,
        'download_links': download_links[:1],
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
