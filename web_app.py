import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from analyzer import analyze_log

app = FastAPI()


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

        <button type="submit">Analyze</button>
    </form>
    """

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    log_file: UploadFile = File(...),
    level_filter: str = Form(""),
    last_count: int = Form(3),
):
    if level_filter == "":
        level_filter = None

    content = await log_file.read()

    with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    stats = analyze_log(temp_file_path, level_filter)

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
    <p>Total lines: {stats["total_lines"]}</p>
    <p>Total problems: {len(stats["problem_lines"])}</p>
    <p>Total errors: {stats["errors"]}</p>
    <p>Total warnings: {stats["warnings"]}</p>
    <p>Total critical: {stats["critical"]}</p>

    <a href="/">Back</a>
    """