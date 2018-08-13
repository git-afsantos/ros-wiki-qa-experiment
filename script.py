import json
import os

DATA_ROOT = "data/project"

HTML_QA_TEMPLATE = """
                      <div id="{distro}qa-panel" class="dropdown qa-panel">
                        <p class="qa-header">Summary</p>
                        <table class="qa-summary-table">
                          <tbody>
                            <tr>
                              <td>Overall Score</td>
                              <td class="qa-overall-score">{score_stars}
                              </td>
                            </tr>
                            <tr>
                              <td>User Rating</td>
                              <td class="qa-user-rating">{user_stars}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <ul class="qa-warnings" style="display:block;">{warnings}
                        </ul>
                        <p class="qa-header">Metrics</p>
                        <table class="qa-metrics-table">
                          <thead>
                            <tr>
                              <th>Metric</th>
                              <th>Value</th>
                              <th>Min.</th>
                              <th>Max.</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>Lines of Code</td>
                              <td data-metric="loc">{loc}</td>
                              <td>0</td><td>-</td>
                            </tr>
                            <tr>
                              <td>Comment/Code Ratio</td>
                              <td data-metric="comment_ratio">{comment_ratio}</td>
                              <td>20%</td><td>-</td>
                            </tr>
                            <tr>
                              <td>Cyclomatic Complexity (avg.)</td>
                              <td data-metric="cyclomatic_complexity">{cyclomatic_complexity}</td>
                              <td>1</td><td>15</td>
                            </tr>
                            <tr>
                              <td>Coding Style Violations</td>
                              <td data-metric="coding_violations">{coding_violations}</td>
                              <td>0</td><td>-</td>
                            </tr>
                            <tr>
                              <td>Maintainability Index</td>
                              <td data-metric="maintainability_index">{maintainability_index}</td>
                              <td>1</td><td>100</td>
                            </tr>
                            <tr>
                              <td>Class Coupling (avg.)</td>
                              <td data-metric="class_coupling">{class_coupling}</td>
                              <td>0</td><td>5</td>
                            </tr>
                            <tr>
                              <td>Depth of Inheritance (avg.)</td>
                              <td data-metric="depth_inheritance">{depth_inheritance}</td>
                              <td>0</td><td>5</td>
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
    return HTML_QA_TEMPLATE.format(
        distro=distro,
        score_stars=gen_html_stars(0),
        user_stars=gen_html_stars(0),
        warnings=gen_html_warnings([]),
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
