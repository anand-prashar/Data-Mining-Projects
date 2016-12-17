import collections

def load_graph(g):
    """
    g should be an iterable which each iteration gives one line
    """

    if not isinstance(g, collections.Iterable):
        raise TypeError('g must be iterable')

    problem_defined = False
    vertices = None
    edges = []
    num_edges = None

    for line in g:
        line = line.strip()
        if not line: # ignore empty lines
            continue

        if line[0] == 'c': # comment line
            continue

        l = line.split()

        if line[0] == 'p':  # problem line
            problem_defined = True
            vertices = [None for i in range(int(l[1]))] # l[1] number of vertices
            num_edges = int(l[2]) # l[2] number of edges

        elif line[0] == 'v': # vertex description
            if not problem_defined:
                raise ValueError('Vertex is defined before problem is defined')

            v_id = int(l[1]) # vertex id
            if v_id < 1 or v_id > len(vertices):
                raise ValueError('Vertex ID too small or too large (must range between 1 to the number of vertices)')

            if vertices[v_id - 1]:
                raise ValueError('Multiple definition of vertex {}'.format(v_id))

            vertices[v_id - 1] = int(l[2])

        elif line[0] == 'e': # edge description
            if not problem_defined:
                raise ValueError('Edge is defined before problem is defined')

            v0 = int(l[1])
            v1 = int(l[2])

            if v0 < 1 or v0 > len(vertices) or v1 < 1 or v1 > len(vertices):
                raise ValueError('Vertex ID too small or too large (must range between 1 to the number of vertices)')

            if len(edges) >= num_edges:
                raise ValueError('Too many edges specified!')

            edges.append((v0, v1))

    if not problem_defined:
        raise ValueError('No problem defined!')

    if len(edges) != num_edges:
        raise ValueError('Edge number incorrect')

    for v in vertices:
        if not v:
            raise ValueError('Vertex number incorrect')

    return vertices, edges
