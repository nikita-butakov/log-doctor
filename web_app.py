import tempfile
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from analyzer import analyze_log
from openai import OpenAI

app = FastAPI()

def explain_with_ai(stats, last_count, level_filter):
    client = OpenAI()

    problems = stats["problem_lines"][-last_count:]

    if level_filter is None:
        level_text = "ALL"
    else:
        level_text = level_filter

    prompt = f"""
You are helping a beginner DevOps engineer understand log errors.

Log level filter: {level_text}

Explain these log lines:
{chr(10).join(problems)}

Give:
1. Short summary
2. Possible causes
3. First 3 checks to do
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    return response.output_text


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Log Doctor</h1>

    <form action="/analyze" method="post" enctype="multipart/form-data">
        <label>Upload log file:</label><br>
        <input type="file" name="log_file"><br><br>

        <label>Level:</label><br>
        <select name="level_filter">
            <option value="">ALL</option>
            <option value="ERROR">ERROR</option>
            <option value="WARNING">WARNING</option>
            <option value="CRITICAL">CRITICAL</option>
        </select><br><br>

        <label>Last problems count:</label><br>
        <input type="number" name="last_count" value="3" min="1"><br><br>
        
        <label>
            <input type="checkbox" name="use_ai" value="true">
            Use AI explanation
        </label><br><br>

        <button type="submit">Analyze</button>
    </form>
    """

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    log_file: UploadFile = File(...),
    level_filter: str = Form(""),
    last_count: int = Form(3),
    use_ai: str = Form(None),
):
    if level_filter == "":
        level_filter = None

    if last_count <= 0:
        return """
        <h1>Error</h1>
        <p>Last problems count must be greater than 0.</p>
        <a href="/">Back</a>
        """

    content = await log_file.read()

    with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        stats = analyze_log(temp_file_path, level_filter)
    finally:
        os.remove(temp_file_path)

    if stats["total_lines"] == 0:
        return """
        <h1>Error</h1>
        <p>Uploaded log file is empty.</p>
        <a href="/">Back</a>
        """

    ai_html = ""

    if use_ai and stats["problem_lines"]:
        try:
            ai_explanation = explain_with_ai(stats, last_count, level_filter)
            ai_html = f"""
            <h2>AI Explanation</h2>
            <pre>{ai_explanation}</pre>
            """
        except Exception as error:
            ai_html = f"""
            <h2>AI Explanation</h2>
            <p>AI explanation failed: {error}</p>
            """
    elif use_ai:
        ai_html = """
        <h2>AI Explanation</h2>
        <p>AI explanation skipped: no problems found.</p>
        """

    problems_html = ""

    if stats["problem_lines"]:
        for problem in stats["problem_lines"][-last_count:]:
            problems_html += f"<li>{problem}</li>"
    else:
        problems_html = "<li>No problems found.</li>"

    return f"""
    <h1>Result</h1>

    <h2>Last {last_count} problems</h2>
    <ul>
        {problems_html}
    </ul>

    <h2>Summary</h2>
    <p>Level filter: {level_filter or "ALL"}</p>
    <p>Use AI: {bool(use_ai)}</p>
    <p>Total lines: {stats["total_lines"]}</p>
    <p>Total problems: {len(stats["problem_lines"])}</p>
    <p>Total errors: {stats["errors"]}</p>
    <p>Total warnings: {stats["warnings"]}</p>
    <p>Total critical: {stats["critical"]}</p>
    
    {ai_html}

    <a href="/">Back</a>
    """