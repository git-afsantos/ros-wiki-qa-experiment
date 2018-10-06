import json
import os

DATA_ROOT = "data/project"

HTML_INFO_TEMPLATE = """
                      <div class="pkg-top-summary">
                        <p id="package-info-{psn1}">{description1}</p>
                        <p id="package-info-{psn2}">{description2}</p>
                        <ul>
                          <li>Maintainer status: {maint_status}</li>
                          <li>Maintainer: {maint}</li>
                          <li>Author: {author}</li>
                          <li>License: {license}</li>
                          <li>Source: {source}</li>
                          <li>QA Score: {score_stars}</li>
                          <li>User Rating: {user_stars}</li>
                        </ul>
                      </div>
"""

HTML_QA_TEMPLATE = """
                      <div id="{distro}qa-panel" class="qa-panel">
                        <ul class="qa-warnings" style="display:block;">{warnings}
                        </ul>
                        <p class="qa-header">Metrics</p>
                        <table class="qa-metrics-table">
                          <thead>
                            <tr>
                              <th>Metric</th>
                              <th><span title="">Latest</span></th>
                              {prev_versions}
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>Lines of Code</td>
                              <td data-metric="loc">{loc}</td>
                              {prev_loc}
                            </tr>
                            <tr>
                              <td>Comment/Code Ratio</td>
                              <td data-metric="comment_ratio">{comment_ratio}</td>
                              {prev_comment_ratio}
                            </tr>
                            <tr>
                              <td>Cyclomatic Complexity (avg.)</td>
                              <td data-metric="cyclomatic_complexity">{cyclomatic_complexity}</td>
                              {prev_cyclomatic_complexity}
                            </tr>
                            <tr>
                              <td>Coding Style Violations</td>
                              <td data-metric="coding_violations">{coding_violations}</td>
                              {prev_coding_violations}
                            </tr>
                            <tr>
                              <td>Maintainability Index</td>
                              <td data-metric="maintainability_index">{maintainability_index}</td>
                              {prev_maintainability_index}
                            </tr>
                            <tr>
                              <td>Class Coupling (avg.)</td>
                              <td data-metric="class_coupling">{class_coupling}</td>
                              {prev_class_coupling}
                            </tr>
                            <tr>
                              <td>Depth of Inheritance (avg.)</td>
                              <td data-metric="depth_inheritance">{depth_inheritance}</td>
                              {prev_depth_inheritance}
                            </tr>
                          </tbody>
                        </table>
                      </div>"""


def from_json_to_html(distro, package_name):
    violations_file = os.path.join(DATA_ROOT, "compliance",
                                   package_name + ".json")
    metrics_file = os.path.join(DATA_ROOT, "metrics", package_name + ".json")
    with open(violations_file, "r") as json_file:
        violations_data = json.load(json_file)
    with open(metrics_file, "r") as json_file:
        metrics_data = json.load(json_file)
    metrics = get_interesting_metrics(metrics_data)
    metrics["coding_violations"] = str(len(violations_data))
    s = HTML_INFO_TEMPLATE.format(psn1 = "1", description1 = "",
        psn2 = "2", description2 = "", maint_status = "developed",
        maint = "Maintainer", author = "Author", license = "BSD",
        source = "git <a>github</a> (branch: ...)",
        score_stars = gen_html_stars(0),
        user_stars = gen_html_stars(0))
    return s + HTML_QA_TEMPLATE.format(
        distro=distro,
        warnings=gen_html_warnings([]),
        **gen_html_versions(),
        **gen_html_previous_metrics(),
        **metrics
    )

def get_interesting_metrics(data):
    sloc = 0
    ratios = []
    cc = []
    mi = []
    coupling = []
    dit = []
    for datum in data:
        metric = datum["metric"]
        value = datum["value"]
        if metric == "sloc":
            sloc += value
        elif metric == "comment_ratio":
            ratios.append(value)
        elif metric == "cyclomatic_complexity":
            cc.append(value)
        elif metric == "maintainability_index":
            mi.append(value)
        elif metric == "class_coupling":
            coupling.append(value)
        elif metric == "depth_inheritance":
            dit.append(value)
    sloc = str(sloc)
    ratios = avg(ratios)
    ratios = str(ratios) if not ratios is None else ""
    cc = avg(cc)
    cc = str(round(cc)) if not cc is None else ""
    mi = avg(mi)
    mi = str(round(mi)) if not mi is None else ""
    coupling = avg(coupling)
    coupling = str(coupling) if not coupling is None else ""
    dit = avg(dit)
    dit = str(dit) if not dit is None else ""
    return {
        "loc": sloc,
        "comment_ratio": ratios,
        "cyclomatic_complexity": cc,
        "maintainability_index": mi,
        "class_coupling": coupling,
        "depth_inheritance": dit
    }

def avg(xs):
    if not xs:
        return None
    return sum(xs) / float(len(xs))


def gen_html_stars(n):
    html = ""
    for i in xrange(n):
        html += ("                                "
                 '<span class="glyphicon glyphicon-star"></span>\n')
    for i in xrange(n, 5):
        html += ("                                "
                 '<span class="glyphicon glyphicon-star-empty"></span>\n')
    return html

def gen_html_warnings(warnings):
    html = ""
    for warning in warnings:
        html += ("\n                          "
                 + '<li><span class="glyphicon glyphicon-warning-sign"></span> '
                 + warning + "</li>")
    return html

def gen_html_versions():
    pass

def gen_html_previous_metrics():
    pass
