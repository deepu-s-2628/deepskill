"""
Flowchart Generation Utility for PM Feature Agent.

This module provides helpers for creating professional visual flowcharts
using Graphviz. The LLM should use these to design feature-specific
flowcharts in custom build scripts.

Usage (in a custom build_documents.py):
    import sys
    sys.path.insert(0, '/path/to/Templates')
    from generate_flowchart import FlowchartBuilder, MultiPageFlowchart

Requirements:
    pip install graphviz
    Also requires Graphviz system package:
        brew install graphviz  (macOS)
        apt-get install graphviz  (Ubuntu)

Fallback (if graphviz not available):
    pip install matplotlib
    Uses matplotlib patches to draw flowcharts
"""

from pathlib import Path

try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False


# ═══════════════════════════════════════════════════════════
# COLOR SCHEMES
# ═══════════════════════════════════════════════════════════

class FlowColors:
    """Color palette for flowchart elements."""
    # Node fills
    START_END = '#C8E6C9'       # Light green
    PROCESS = '#E3F2FD'         # Light blue
    DECISION = '#FFF3E0'        # Light orange
    ALERT = '#FFCDD2'           # Light red
    DATA = '#E1BEE7'           # Light purple
    EXTERNAL = '#F5F5F5'        # Light gray

    # Node borders
    START_END_BORDER = '#388E3C'
    PROCESS_BORDER = '#1976D2'
    DECISION_BORDER = '#F57C00'
    ALERT_BORDER = '#D32F2F'
    DATA_BORDER = '#7B1FA2'
    EXTERNAL_BORDER = '#616161'

    # Edge colors
    EDGE_DEFAULT = '#37474F'
    EDGE_SUCCESS = '#388E3C'
    EDGE_FAILURE = '#D32F2F'
    EDGE_OPTIONAL = '#78909C'

    # Background
    BACKGROUND = '#FFFFFF'
    SUBGRAPH_BG = '#FAFAFA'


class EnhancementColors:
    """Color palette for enhancement flowcharts (before/after)."""
    # Existing / unchanged elements (green)
    EXISTING_FILL = '#C8E6C9'
    EXISTING_BORDER = '#388E3C'
    EXISTING_EDGE = '#388E3C'

    # New elements added by enhancement (blue)
    NEW_FILL = '#E3F2FD'
    NEW_BORDER = '#1976D2'
    NEW_EDGE = '#1976D2'

    # Modified elements (orange)
    MODIFIED_FILL = '#FFF3E0'
    MODIFIED_BORDER = '#F57C00'
    MODIFIED_EDGE = '#F57C00'

    # Removed elements (red, dashed)
    REMOVED_FILL = '#FFCDD2'
    REMOVED_BORDER = '#D32F2F'

    # Legend
    LEGEND_BG = '#FAFAFA'


# ═══════════════════════════════════════════════════════════
# FLOWCHART BUILDER
# ═══════════════════════════════════════════════════════════

class FlowchartBuilder:
    """
    Build professional flowcharts using Graphviz.

    Example:
        fb = FlowchartBuilder("Feature Setup Flow")
        fb.start_node("begin", "Start")
        fb.process_node("discover", "Discover Devices")
        fb.decision_node("found", "Devices\\nFound?")
        fb.process_node("configure", "Apply Monitors")
        fb.end_node("done", "Setup Complete")

        fb.edge("begin", "discover")
        fb.edge("discover", "found")
        fb.success_edge("found", "configure")
        fb.failure_edge("found", "begin")
        fb.edge("configure", "done")

        fb.render("output/setup_flow.pdf")
    """

    def __init__(self, title="Flowchart", direction="TB", engine="dot"):
        """
        Initialize the flowchart.
        direction: TB (top-bottom), LR (left-right), BT, RL
        engine: dot, neato, fdp, circo, twopi
        """
        if not HAS_GRAPHVIZ:
            raise ImportError(
                "Graphviz Python package not installed. Run: pip install graphviz\n"
                "Also install system package: brew install graphviz"
            )

        self.graph = graphviz.Digraph(title, format='pdf', engine=engine)
        self.graph.attr(
            rankdir=direction,
            size='11,8.5',
            dpi='150',
            bgcolor=FlowColors.BACKGROUND,
            pad='0.5',
            nodesep='0.6',
            ranksep='0.8',
            label=f'<<B>{title}</B>>',
            labelloc='t',
            fontname='Segoe UI',
            fontsize='16',
        )
        self.graph.attr('node',
            fontname='Segoe UI',
            fontsize='11',
            margin='0.3,0.15',
        )
        self.graph.attr('edge',
            fontname='Segoe UI',
            fontsize='9',
            color=FlowColors.EDGE_DEFAULT,
            arrowsize='0.8',
        )
        self.title = title
        self._subgraphs = {}

    # ─── NODE TYPES ────────────────────────────────────────

    def start_node(self, node_id, label="Start"):
        """Oval start node (green)."""
        self.graph.node(node_id, label,
            shape='oval',
            style='filled',
            fillcolor=FlowColors.START_END,
            color=FlowColors.START_END_BORDER,
            penwidth='2',
        )

    def end_node(self, node_id, label="End"):
        """Oval end node (green)."""
        self.graph.node(node_id, label,
            shape='oval',
            style='filled',
            fillcolor=FlowColors.START_END,
            color=FlowColors.START_END_BORDER,
            penwidth='2',
        )

    def process_node(self, node_id, label):
        """Rounded rectangle process node (blue)."""
        self.graph.node(node_id, label,
            shape='box',
            style='filled,rounded',
            fillcolor=FlowColors.PROCESS,
            color=FlowColors.PROCESS_BORDER,
            penwidth='1.5',
        )

    def decision_node(self, node_id, label):
        """Diamond decision node (orange)."""
        self.graph.node(node_id, label,
            shape='diamond',
            style='filled',
            fillcolor=FlowColors.DECISION,
            color=FlowColors.DECISION_BORDER,
            penwidth='1.5',
            width='2',
            height='1.2',
        )

    def alert_node(self, node_id, label):
        """Hexagon alert/warning node (red)."""
        self.graph.node(node_id, label,
            shape='hexagon',
            style='filled',
            fillcolor=FlowColors.ALERT,
            color=FlowColors.ALERT_BORDER,
            penwidth='1.5',
        )

    def data_node(self, node_id, label):
        """Cylinder data/storage node (purple)."""
        self.graph.node(node_id, label,
            shape='cylinder',
            style='filled',
            fillcolor=FlowColors.DATA,
            color=FlowColors.DATA_BORDER,
            penwidth='1.5',
        )

    def external_node(self, node_id, label):
        """Double-bordered external system node (gray)."""
        self.graph.node(node_id, label,
            shape='box',
            style='filled',
            fillcolor=FlowColors.EXTERNAL,
            color=FlowColors.EXTERNAL_BORDER,
            penwidth='1.5',
            peripheries='2',
        )

    def io_node(self, node_id, label):
        """Parallelogram I/O node (purple)."""
        self.graph.node(node_id, label,
            shape='parallelogram',
            style='filled',
            fillcolor=FlowColors.DATA,
            color=FlowColors.DATA_BORDER,
            penwidth='1.5',
        )

    # ─── EDGES ─────────────────────────────────────────────

    def edge(self, from_id, to_id, label="", style="solid", color=None):
        """Add an edge between nodes."""
        attrs = {}
        if label:
            attrs['label'] = f'  {label}  '
        if color:
            attrs['color'] = color
            attrs['fontcolor'] = color
        if style == "dashed":
            attrs['style'] = 'dashed'
            if 'color' not in attrs:
                attrs['color'] = FlowColors.EDGE_OPTIONAL
        self.graph.edge(from_id, to_id, **attrs)

    def success_edge(self, from_id, to_id, label="Yes"):
        """Green edge for success/positive path."""
        self.edge(from_id, to_id, label, color=FlowColors.EDGE_SUCCESS)

    def failure_edge(self, from_id, to_id, label="No"):
        """Red edge for failure/negative path."""
        self.edge(from_id, to_id, label, color=FlowColors.EDGE_FAILURE)

    def optional_edge(self, from_id, to_id, label=""):
        """Dashed edge for optional/alternative paths."""
        self.edge(from_id, to_id, label, style="dashed")

    # ─── SUBGRAPHS ─────────────────────────────────────────

    def begin_subgraph(self, name, label=""):
        """Create a subgraph (cluster) for grouping nodes."""
        sg = graphviz.Digraph(f'cluster_{name}')
        sg.attr(
            label=label,
            style='rounded,dashed',
            color='#90A4AE',
            bgcolor=FlowColors.SUBGRAPH_BG,
            fontname='Segoe UI',
            fontsize='12',
            labeljust='l',
            penwidth='1.5',
        )
        self._subgraphs[name] = sg
        return sg

    def end_subgraph(self, name):
        """Add the subgraph to the main graph."""
        if name in self._subgraphs:
            self.graph.subgraph(self._subgraphs[name])

    # ─── ENHANCEMENT-SPECIFIC NODES ────────────────────────

    def existing_node(self, node_id, label):
        """Green node for existing/unchanged steps (enhancement flows)."""
        self.graph.node(node_id, label,
            shape='box',
            style='filled,rounded',
            fillcolor=EnhancementColors.EXISTING_FILL,
            color=EnhancementColors.EXISTING_BORDER,
            penwidth='1.5',
        )

    def new_node(self, node_id, label):
        """Blue dashed node for new steps added by enhancement."""
        self.graph.node(node_id, label,
            shape='box',
            style='filled,rounded,dashed',
            fillcolor=EnhancementColors.NEW_FILL,
            color=EnhancementColors.NEW_BORDER,
            penwidth='2.5',
        )

    def modified_node(self, node_id, label):
        """Orange bold-border node for modified steps."""
        self.graph.node(node_id, label,
            shape='box',
            style='filled,rounded,bold',
            fillcolor=EnhancementColors.MODIFIED_FILL,
            color=EnhancementColors.MODIFIED_BORDER,
            penwidth='3',
        )

    def removed_node(self, node_id, label):
        """Red strikethrough node for deprecated/removed steps."""
        self.graph.node(node_id, label,
            shape='box',
            style='filled,rounded,dashed',
            fillcolor=EnhancementColors.REMOVED_FILL,
            color=EnhancementColors.REMOVED_BORDER,
            penwidth='1.5',
            fontcolor='#999999',
        )

    def existing_edge(self, from_id, to_id, label=""):
        """Green edge for existing connections."""
        self.edge(from_id, to_id, label, color=EnhancementColors.EXISTING_EDGE)

    def new_edge(self, from_id, to_id, label=""):
        """Blue dashed edge for new connections."""
        attrs = {'style': 'dashed', 'color': EnhancementColors.NEW_EDGE,
                 'fontcolor': EnhancementColors.NEW_EDGE, 'penwidth': '2'}
        if label:
            attrs['label'] = f'  {label}  '
        self.graph.edge(from_id, to_id, **attrs)

    def modified_edge(self, from_id, to_id, label=""):
        """Orange edge for modified connections."""
        self.edge(from_id, to_id, label, color=EnhancementColors.MODIFIED_EDGE)

    # ─── LEGEND ────────────────────────────────────────────

    def add_legend(self, items=None):
        """
        Add a color legend to the flowchart.
        items: list of tuples (label, fill_color, border_color)
               If None, uses default enhancement legend.
        """
        if items is None:
            items = [
                ('Existing (unchanged)', EnhancementColors.EXISTING_FILL,
                 EnhancementColors.EXISTING_BORDER),
                ('New (added)', EnhancementColors.NEW_FILL,
                 EnhancementColors.NEW_BORDER),
                ('Modified (changed)', EnhancementColors.MODIFIED_FILL,
                 EnhancementColors.MODIFIED_BORDER),
                ('Removed (deprecated)', EnhancementColors.REMOVED_FILL,
                 EnhancementColors.REMOVED_BORDER),
            ]

        legend = graphviz.Digraph('cluster_legend')
        legend.attr(
            label='Legend',
            style='rounded',
            color='#90A4AE',
            bgcolor=EnhancementColors.LEGEND_BG,
            fontname='Segoe UI',
            fontsize='11',
            labeljust='l',
            penwidth='1',
        )

        for i, (label, fill, border) in enumerate(items):
            node_id = f'legend_{i}'
            legend.node(node_id, label,
                shape='box',
                style='filled,rounded',
                fillcolor=fill,
                color=border,
                penwidth='1.5',
                fontsize='9',
                width='2',
                height='0.3',
            )
            if i > 0:
                prev_id = f'legend_{i - 1}'
                legend.edge(prev_id, node_id, style='invis')

        self.graph.subgraph(legend)

    # ─── RENDERING ─────────────────────────────────────────

    def render(self, output_path, cleanup=True):
        """Render the flowchart to file (PDF, PNG, or SVG based on extension)."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        format_type = path.suffix.lstrip('.')
        if format_type not in ('pdf', 'png', 'svg'):
            format_type = 'pdf'

        self.graph.format = format_type
        output_file = str(path.with_suffix(''))
        self.graph.render(output_file, cleanup=cleanup)
        print(f"✅ Generated flowchart: {path}")
        return path

    def render_png(self, output_path):
        """Render as high-res PNG (useful for embedding in PPTX)."""
        path = Path(output_path).with_suffix('.png')
        path.parent.mkdir(parents=True, exist_ok=True)
        self.graph.format = 'png'
        self.graph.attr(dpi='200')
        self.graph.render(str(path.with_suffix('')), cleanup=True)
        print(f"✅ Generated PNG: {path}")
        return path


# ═══════════════════════════════════════════════════════════
# MULTI-PAGE PDF BUILDER
# ═══════════════════════════════════════════════════════════

class MultiPageFlowchart:
    """
    Build a multi-page flowchart PDF with different diagrams per page.

    Example:
        mpf = MultiPageFlowchart()
        mpf.add_page(setup_flowchart)       # FlowchartBuilder instance
        mpf.add_page(data_flow_chart)       # Another FlowchartBuilder
        mpf.add_page(alert_flow_chart)      # Another one
        mpf.render("output/feature_flowchart.pdf")
    """

    def __init__(self):
        self.pages = []

    def add_page(self, flowchart_builder):
        """Add a FlowchartBuilder as a page."""
        self.pages.append(flowchart_builder)

    def render(self, output_path):
        """Render all pages into a single or multiple PDFs."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if len(self.pages) == 1:
            self.pages[0].render(str(path))
            return path

        # Render individual pages
        page_files = []
        for i, page in enumerate(self.pages):
            page_path = path.parent / f"_page_{i}.pdf"
            page.render(str(page_path))
            page_files.append(page_path)

        # Try to merge with pypdf
        try:
            from pypdf import PdfMerger
            merger = PdfMerger()
            for pf in page_files:
                merger.append(str(pf))
            merger.write(str(path))
            merger.close()
            for pf in page_files:
                pf.unlink(missing_ok=True)
            print(f"✅ Generated multi-page flowchart: {path}")
        except ImportError:
            # If no merger available, keep first page as main
            print(f"⚠️  pypdf not available — generated {len(page_files)} separate PDF pages")
            if page_files:
                page_files[0].rename(path)

        return path


# ═══════════════════════════════════════════════════════════
# SWIMLANE DIAGRAM BUILDER
# ═══════════════════════════════════════════════════════════

class SwimlaneDiagram:
    """
    Build responsibility-based swimlane diagrams.

    Example:
        swim = SwimlaneDiagram("Alert Processing Flow")
        swim.add_lane("User", "#E3F2FD")
        swim.add_lane("OpManager", "#E8F5E9")
        swim.add_lane("External", "#FFF3E0")

        swim.add_node("User", "user_sees", "User sees alert", "process")
        swim.add_node("OpManager", "eval_threshold", "Evaluate\\nThreshold", "decision")
        swim.add_node("External", "send_ticket", "Create Ticket", "process")

        swim.add_edge("user_sees", "eval_threshold")
        swim.add_edge("eval_threshold", "send_ticket", "Exceeded")

        swim.render("output/swimlane.pdf")
    """

    def __init__(self, title="Swimlane Diagram", direction="TB"):
        if not HAS_GRAPHVIZ:
            raise ImportError("Graphviz not installed.")

        self.title = title
        self.direction = direction
        self.lanes = []  # list of (name, color)
        self.nodes = {}  # lane_name -> [(node_id, label, node_type)]
        self.edges = []  # (from_id, to_id, label, style)

    def add_lane(self, name, color="#E3F2FD"):
        """Add a swimlane."""
        self.lanes.append((name, color))
        if name not in self.nodes:
            self.nodes[name] = []

    def add_node(self, lane, node_id, label, node_type="process"):
        """
        Add a node to a lane.
        node_type: 'start', 'end', 'process', 'decision', 'alert', 'data'
        """
        if lane not in self.nodes:
            self.nodes[lane] = []
        self.nodes[lane].append((node_id, label, node_type))

    def add_edge(self, from_id, to_id, label="", style="solid"):
        """Add an edge."""
        self.edges.append((from_id, to_id, label, style))

    def render(self, output_path):
        """Render the swimlane diagram."""
        graph = graphviz.Digraph(self.title, format='pdf', engine='dot')
        graph.attr(
            rankdir=self.direction,
            size='11,8.5',
            dpi='150',
            label=f'<<B>{self.title}</B>>',
            labelloc='t',
            fontname='Segoe UI',
            fontsize='16',
            compound='true',
        )
        graph.attr('node', fontname='Segoe UI', fontsize='10', margin='0.3,0.15')
        graph.attr('edge', fontname='Segoe UI', fontsize='9',
                   color=FlowColors.EDGE_DEFAULT, arrowsize='0.8')

        node_styles = {
            'start': {'shape': 'oval', 'fillcolor': FlowColors.START_END,
                      'color': FlowColors.START_END_BORDER},
            'end': {'shape': 'oval', 'fillcolor': FlowColors.START_END,
                    'color': FlowColors.START_END_BORDER},
            'process': {'shape': 'box', 'fillcolor': FlowColors.PROCESS,
                        'color': FlowColors.PROCESS_BORDER},
            'decision': {'shape': 'diamond', 'fillcolor': FlowColors.DECISION,
                         'color': FlowColors.DECISION_BORDER},
            'alert': {'shape': 'hexagon', 'fillcolor': FlowColors.ALERT,
                      'color': FlowColors.ALERT_BORDER},
            'data': {'shape': 'cylinder', 'fillcolor': FlowColors.DATA,
                     'color': FlowColors.DATA_BORDER},
        }

        for lane_name, lane_color in self.lanes:
            with graph.subgraph(name=f'cluster_{lane_name}') as sg:
                sg.attr(
                    label=f'  {lane_name}  ',
                    style='rounded,filled',
                    color='#90A4AE',
                    fillcolor=lane_color,
                    fontname='Segoe UI',
                    fontsize='12',
                    fontcolor='#37474F',
                    labeljust='l',
                    penwidth='1.5',
                )
                for node_id, label, node_type in self.nodes.get(lane_name, []):
                    style_attrs = node_styles.get(node_type, node_styles['process'])
                    sg.node(node_id, label,
                            shape=style_attrs['shape'],
                            style='filled,rounded',
                            fillcolor=style_attrs['fillcolor'],
                            color=style_attrs['color'],
                            penwidth='1.5')

        for from_id, to_id, label, style in self.edges:
            attrs = {}
            if label:
                attrs['label'] = f'  {label}  '
            if style == 'dashed':
                attrs['style'] = 'dashed'
                attrs['color'] = FlowColors.EDGE_OPTIONAL
            graph.edge(from_id, to_id, **attrs)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        graph.render(str(path.with_suffix('')), cleanup=True)
        print(f"✅ Generated swimlane: {path}")
        return path


# ═══════════════════════════════════════════════════════════
# MERMAID → GRAPHVIZ TRANSLATOR
# ═══════════════════════════════════════════════════════════

def mermaid_to_flowchart(mermaid_text, title="Flowchart"):
    """
    Translate basic Mermaid flowchart syntax to a FlowchartBuilder.

    Supports:
        flowchart TD / LR
        A[Label]           → process node
        A{Label}           → decision node
        A([Label])         → start/end (stadium shape)
        A((Label))         → start/end (circle)
        A[(Label)]         → data node (cylinder)
        A --> B             → edge
        A -->|label| B      → labeled edge
        A -.-> B            → dashed edge
        A ==> B             → thick edge
        subgraph Name       → subgraph
        end                 → end subgraph

    Returns a FlowchartBuilder instance ready to render.
    """
    if not HAS_GRAPHVIZ:
        raise ImportError(
            "Graphviz required for Mermaid translation. "
            "Run: pip install graphviz && brew install graphviz"
        )

    import re

    lines = mermaid_text.strip().split('\n')
    direction = 'TB'
    nodes = {}  # id -> (label, type)
    edges = []
    subgraphs = {}  # name -> [node_ids]
    current_subgraph = None

    # Parse direction
    first_line = lines[0].strip().lower()
    if 'lr' in first_line:
        direction = 'LR'
    elif 'bt' in first_line:
        direction = 'BT'
    elif 'rl' in first_line:
        direction = 'RL'

    node_patterns = [
        (r'(\w+)\(\[(.+?)\]\)', 'start'),      # A([Label]) - stadium
        (r'(\w+)\(\((.+?)\)\)', 'start'),       # A((Label)) - circle
        (r'(\w+)\[\((.+?)\)\]', 'data'),        # A[(Label)] - cylinder
        (r'(\w+)\{(.+?)\}', 'decision'),        # A{Label} - diamond
        (r'(\w+)\[(.+?)\]', 'process'),         # A[Label] - box
    ]

    def extract_node(text):
        """Extract node ID and details from text fragment."""
        text = text.strip()
        for pattern, node_type in node_patterns:
            m = re.match(pattern, text)
            if m:
                return m.group(1), m.group(2), node_type
        # Plain ID (no shape)
        m = re.match(r'(\w+)', text)
        if m:
            return m.group(1), m.group(1), 'process'
        return None, None, None

    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith('%%'):
            continue

        # Subgraph
        if line.lower().startswith('subgraph'):
            sg_name = line[8:].strip().strip('"').strip("'")
            current_subgraph = sg_name
            subgraphs[sg_name] = []
            continue

        if line.lower() == 'end':
            current_subgraph = None
            continue

        # Edges: A -->|label| B, A --> B, A -.-> B, A ==> B
        edge_patterns = [
            (r'(.+?)\s*-->\|(.+?)\|\s*(.+)', 'solid'),
            (r'(.+?)\s*-->\s*(.+)', 'solid'),
            (r'(.+?)\s*-\.->(?:\|(.+?)\|)?\s*(.+)', 'dashed'),
            (r'(.+?)\s*==>\s*(.+)', 'solid'),
        ]

        matched = False
        for pattern, style in edge_patterns:
            m = re.match(pattern, line)
            if m:
                groups = m.groups()
                if len(groups) == 3:
                    left_text, label, right_text = groups
                else:
                    left_text, right_text = groups[0], groups[1]
                    label = ""

                from_id, from_label, from_type = extract_node(left_text)
                to_id, to_label, to_type = extract_node(right_text)

                if from_id and from_id not in nodes:
                    nodes[from_id] = (from_label, from_type)
                    if current_subgraph:
                        subgraphs[current_subgraph].append(from_id)

                if to_id and to_id not in nodes:
                    nodes[to_id] = (to_label, to_type)
                    if current_subgraph:
                        subgraphs[current_subgraph].append(to_id)

                if from_id and to_id:
                    edges.append((from_id, to_id, label or "", style))

                matched = True
                break

        if not matched:
            # Standalone node definition
            node_id, node_label, node_type = extract_node(line)
            if node_id and node_id not in nodes:
                nodes[node_id] = (node_label, node_type)
                if current_subgraph:
                    subgraphs[current_subgraph].append(node_id)

    # Build the FlowchartBuilder
    fb = FlowchartBuilder(title, direction=direction)

    # Create subgraphs first
    sg_node_sets = set()
    for sg_name, sg_nodes in subgraphs.items():
        sg = fb.begin_subgraph(sg_name.replace(' ', '_'), label=sg_name)
        for nid in sg_nodes:
            if nid in nodes:
                label, ntype = nodes[nid]
                _add_node_by_type(sg, nid, label, ntype)
                sg_node_sets.add(nid)
        fb.end_subgraph(sg_name.replace(' ', '_'))

    # Add remaining nodes
    node_adders = {
        'start': fb.start_node,
        'end': fb.end_node,
        'process': fb.process_node,
        'decision': fb.decision_node,
        'alert': fb.alert_node,
        'data': fb.data_node,
    }
    for nid, (label, ntype) in nodes.items():
        if nid not in sg_node_sets:
            adder = node_adders.get(ntype, fb.process_node)
            adder(nid, label)

    # Add edges
    for from_id, to_id, label, style in edges:
        if style == 'dashed':
            fb.optional_edge(from_id, to_id, label)
        elif label and 'yes' in label.lower():
            fb.success_edge(from_id, to_id, label)
        elif label and 'no' in label.lower():
            fb.failure_edge(from_id, to_id, label)
        else:
            fb.edge(from_id, to_id, label)

    return fb


def _add_node_by_type(graph_obj, node_id, label, node_type):
    """Helper to add a node to a graphviz graph/subgraph by type."""
    styles = {
        'start': {'shape': 'oval', 'fillcolor': FlowColors.START_END,
                  'color': FlowColors.START_END_BORDER},
        'end': {'shape': 'oval', 'fillcolor': FlowColors.START_END,
                'color': FlowColors.START_END_BORDER},
        'process': {'shape': 'box', 'fillcolor': FlowColors.PROCESS,
                    'color': FlowColors.PROCESS_BORDER},
        'decision': {'shape': 'diamond', 'fillcolor': FlowColors.DECISION,
                     'color': FlowColors.DECISION_BORDER},
        'alert': {'shape': 'hexagon', 'fillcolor': FlowColors.ALERT,
                  'color': FlowColors.ALERT_BORDER},
        'data': {'shape': 'cylinder', 'fillcolor': FlowColors.DATA,
                 'color': FlowColors.DATA_BORDER},
    }
    s = styles.get(node_type, styles['process'])
    graph_obj.node(node_id, label,
                   shape=s['shape'], style='filled,rounded',
                   fillcolor=s['fillcolor'], color=s['color'],
                   penwidth='1.5')
