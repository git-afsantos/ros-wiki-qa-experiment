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
                              <td data-metric="loc">{}</td>
                              <td>0</td>
                              <td>-</td>
                            </tr>
                            <tr>
                              <td>Comment/Code Ratio</td>
                              <td data-metric="comment_ratio"></td>
                              <td>20%</td>
                              <td>-</td>
                            </tr>
                            <tr>
                              <td>Cyclomatic Complexity (avg.)</td>
                              <td data-metric="cyclomatic_complexity"></td>
                              <td>1</td>
                              <td>15</td>
                            </tr>
                            <tr>
                              <td>Coding Style Violations</td>
                              <td data-metric="coding_violations"></td>
                              <td>0</td>
                              <td>-</td>
                            </tr>
                            <tr>
                              <td>Maintainability Index</td>
                              <td data-metric="maintainability_index"></td>
                              <td>1</td>
                              <td>100</td>
                            </tr>
                            <tr>
                              <td>Class Coupling (avg.)</td>
                              <td data-metric="class_coupling"></td>
                              <td>0</td>
                              <td>5</td>
                            </tr>
                            <tr>
                              <td>Depth of Inheritance (avg.)</td>
                              <td data-metric="depth_inheritance"></td>
                              <td>0</td>
                              <td>5</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>"""


def from_json_to_html(package_name):
    violations_file = os.path.join(DATA_ROOT, "compliance",
                                   package_name + ".json")
    metrics_file = os.path.join(DATA_ROOT, "metrics", package_name + ".json")
    with open(violations_file, "r") as json_file:
        violations_data = json.load(json_file)
    with open(metrics_file, "r") as json_file:
        metrics_data = json.load(json_file)
    metrics = get_interesting_metrics(metrics_data)
    metrics["coding_violations"] = len(violations_data)

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
    cc = avg(cc)
    cc = round(cc) if not cc is None else None
    mi = avg(mi)
    mi = round(mi) if not mi is None else None
    return {
        "loc": sloc,
        "comment_ratio": avg(ratios),
        "cyclomatic_complexity": cc,
        "maintainability_index": mi,
        "class_coupling": avg(coupling),
        "depth_inheritance": avg(dit)
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
