#!/usr/bin/env python3
"""
Webhook Server
Provides HTTP endpoints for triggering content generation

Endpoints:
  POST /scan-rss                - Scan RSS feeds
  POST /research/{topic}        - Research a specific topic
  POST /generate-content        - Generate content from latest data
  POST /approve/{content_id}    - Approve specific content
  GET  /status                  - Get system status

Usage:
  python3 webhook_server.py          # Start server on port 5001
  python3 webhook_server.py --port 8080  # Custom port
"""

from flask import Flask, jsonify, request
from pathlib import Path
import subprocess
import json
from datetime import datetime

app = Flask(__name__)

AGENTS_DIR = Path(__file__).parent


@app.route('/status', methods=['GET'])
def status():
    """Get system status"""

    # Check if data files exist
    rss_file = AGENTS_DIR / 'rss_ideas_database.json'
    research_file = AGENTS_DIR / 'research_results_quick.json'
    angles_file = AGENTS_DIR / 'contrarian_angles.json'
    final_file = AGENTS_DIR / 'final_content_output.json'

    status_data = {
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'data_files': {
            'rss_ideas': rss_file.exists(),
            'research': research_file.exists(),
            'angles': angles_file.exists(),
            'final_content': final_file.exists()
        }
    }

    # If final content exists, add summary
    if final_file.exists():
        with open(final_file, 'r') as f:
            final_data = json.load(f)

        status_data['latest_generation'] = {
            'generated_at': final_data['metadata']['generated_at'],
            'total_pieces': final_data['metadata']['total_pieces'],
            'auto_approved': final_data['metadata']['auto_approved'],
            'mode': final_data['metadata']['mode']
        }

    return jsonify(status_data)


@app.route('/scan-rss', methods=['POST'])
def scan_rss():
    """Trigger RSS feed scan"""

    data = request.get_json() or {}
    days_back = data.get('days_back', 7)
    min_score = data.get('min_score', 10)

    try:
        # Run RSS scout
        result = subprocess.run([
            'python3',
            str(AGENTS_DIR / 'rss_content_scout.py'),
            'scan',
            str(days_back),
            str(min_score)
        ], capture_output=True, text=True, cwd=AGENTS_DIR)

        # Load results
        rss_file = AGENTS_DIR / 'rss_ideas_database.json'
        if rss_file.exists():
            with open(rss_file, 'r') as f:
                rss_data = json.load(f)

            return jsonify({
                'status': 'success',
                'ideas_found': len(rss_data.get('ideas', [])),
                'trending_keywords': rss_data.get('trending_keywords', [])[:10],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'status': 'error', 'message': 'No ideas file generated'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/research/<topic>', methods=['POST'])
def research_topic(topic):
    """Research a specific topic"""

    data = request.get_json() or {}
    mode = data.get('mode', 'quick')

    try:
        # Run research agent
        result = subprocess.run([
            'python3',
            str(AGENTS_DIR / 'research_data_agent.py'),
            'single',
            topic,
            mode
        ], capture_output=True, text=True, cwd=AGENTS_DIR)

        return jsonify({
            'status': 'success',
            'topic': topic,
            'mode': mode,
            'message': 'Research completed',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/generate-content', methods=['POST'])
def generate_content():
    """Generate content from latest data"""

    data = request.get_json() or {}
    mode = data.get('mode', 'balanced')
    auto_approve = data.get('auto_approve', True)

    try:
        # Run orchestrator
        result = subprocess.run([
            'python3',
            str(AGENTS_DIR / 'content_orchestrator.py'),
            '--mode', mode
        ] + (['--no-auto-approve'] if not auto_approve else []),
            capture_output=True, text=True, cwd=AGENTS_DIR
        )

        # Load results
        final_file = AGENTS_DIR / 'final_content_output.json'
        if final_file.exists():
            with open(final_file, 'r') as f:
                final_data = json.load(f)

            return jsonify({
                'status': 'success',
                'total_pieces': final_data['metadata']['total_pieces'],
                'auto_approved': final_data['metadata']['auto_approved'],
                'mode': mode,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'status': 'error', 'message': 'No content generated'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/approve/<int:content_id>', methods=['POST'])
def approve_content(content_id):
    """Approve specific content piece"""

    # Load final content
    final_file = AGENTS_DIR / 'final_content_output.json'

    if not final_file.exists():
        return jsonify({'status': 'error', 'message': 'No content to approve'}), 404

    with open(final_file, 'r') as f:
        final_data = json.load(f)

    content_pieces = final_data['content_ready_for_sheets']

    if content_id < 0 or content_id >= len(content_pieces):
        return jsonify({'status': 'error', 'message': 'Invalid content ID'}), 404

    # Mark as approved
    content_pieces[content_id]['auto_approved'] = True
    content_pieces[content_id]['requires_review'] = False
    content_pieces[content_id]['manual_approval_at'] = datetime.now().isoformat()

    # Save back
    with open(final_file, 'w') as f:
        json.dump(final_data, f, indent=2)

    return jsonify({
        'status': 'success',
        'content_id': content_id,
        'title': content_pieces[content_id]['trend_source']['title'],
        'approved': True,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/daily-run', methods=['POST'])
def daily_run():
    """Run complete daily workflow"""

    data = request.get_json() or {}
    mode = data.get('mode', 'balanced')

    try:
        # Run daily generator
        result = subprocess.run([
            'python3',
            str(AGENTS_DIR / 'daily_content_generator.py'),
            '--mode', mode
        ], capture_output=True, text=True, cwd=AGENTS_DIR)

        return jsonify({
            'status': 'success',
            'message': 'Daily workflow completed',
            'mode': mode,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def main():
    import sys

    port = 3022  # Using assigned port for agents directory

    if len(sys.argv) > 1:
        if '--port' in sys.argv:
            port_index = sys.argv.index('--port') + 1
            if port_index < len(sys.argv):
                port = int(sys.argv[port_index])
        elif '--help' in sys.argv:
            print("""
Webhook Server for Content Generation

Endpoints:
  GET  /status                - System status
  POST /scan-rss              - Scan RSS feeds
  POST /research/{topic}      - Research topic
  POST /generate-content      - Generate content
  POST /approve/{content_id}  - Approve content
  POST /daily-run             - Run daily workflow

Usage:
  python3 webhook_server.py              # Start on port 5001
  python3 webhook_server.py --port 8080  # Custom port

Examples:
  # Check status
  curl http://localhost:5001/status

  # Scan RSS feeds
  curl -X POST http://localhost:5001/scan-rss \\
    -H "Content-Type: application/json" \\
    -d '{"days_back": 7, "min_score": 10}'

  # Research topic
  curl -X POST http://localhost:5001/research/AI%20automation \\
    -H "Content-Type: application/json" \\
    -d '{"mode": "quick"}'

  # Generate content
  curl -X POST http://localhost:5001/generate-content \\
    -H "Content-Type: application/json" \\
    -d '{"mode": "balanced", "auto_approve": true}'

  # Run daily workflow
  curl -X POST http://localhost:5001/daily-run \\
    -H "Content-Type: application/json" \\
    -d '{"mode": "balanced"}'
            """)
            return

    print(f"\n🚀 Starting webhook server on port {port}...")
    print(f"\n📡 Available endpoints:")
    print(f"   GET  http://localhost:{port}/status")
    print(f"   POST http://localhost:{port}/scan-rss")
    print(f"   POST http://localhost:{port}/research/<topic>")
    print(f"   POST http://localhost:{port}/generate-content")
    print(f"   POST http://localhost:{port}/approve/<content_id>")
    print(f"   POST http://localhost:{port}/daily-run")
    print(f"\n✅ Server ready!\n")

    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    main()
