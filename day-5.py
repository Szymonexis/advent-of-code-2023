from typing import List, TypedDict
from utils import clear_log, get_lines, log, log_table, profiler


class Vector(TypedDict):
    d: int
    s: int
    r: int
    o: int


VectorMap = List[Vector]


class SeedsAndVectorMaps(TypedDict):
    seeds: list[int]
    vector_maps: list[VectorMap]


def get_seeds(line: str) -> list[int]:
    return map(int, map(str.strip, line.split(':')[1].strip().split(' ')))


def get_map(lines: list[str]) -> VectorMap:
    vector_map: VectorMap = []
    for line in lines:
        [d, s, r] = list(map(int, map(str.strip, line.strip().split(' '))))
        vector_map.append(Vector(d=d, s=s, r=r, o=0))

    for vector in vector_map:
        vector['o'] = vector['d'] - vector['s']

    return sorted(vector_map, key=lambda x: x['s'])


def get_seeds_and_vector_maps() -> SeedsAndVectorMaps:
    lines = get_lines(__file__)
    seeds = get_seeds(lines[0])

    section_indexes = []
    off = 3
    for i in range(off, len(lines[off:])):
        if lines[i] == '':
            section_indexes.append(i)
    section_indexes.append(len(lines))

    vector_maps = []
    start = 1
    for section_index in section_indexes:
        map_lines = lines[start + 2:section_index]
        vector_maps.append(get_map(map_lines))
        start = section_index

    return SeedsAndVectorMaps(seeds=seeds, vector_maps=vector_maps)


@profiler
def part_one():
    m = get_seeds_and_vector_maps()
    seeds = sorted(m['seeds'])
    vector_maps = m['vector_maps']
    targets = seeds
    
    logs = []
    for v_m in vector_maps:
        i = 0
        j = 0
        n_ts = []
        v_m_l_i = len(v_m) - 1
        while i < len(targets):
            log_dict = {}

            v = v_m[j]
            d = v['d']
            s = v['s']
            o = v['o']
            r = v['r']
            t = targets[i]

            log_dict['s'] = s
            log_dict['o'] = o
            log_dict['r'] = r
            log_dict['t'] = t
            log_dict['i'] = i
            log_dict['j'] = j

            if t < s:
                log_dict['msg'] = 't smaller'
                logs.append(log_dict)

                n_ts.append(t)
                i += 1
                continue

            if s <= t and t < s + r:
                log_dict['msg'] = 't in range'
                logs.append(log_dict)

                n_ts.append(t + o)
                i += 1
                continue

            if s + r <= t and j < v_m_l_i:
                log_dict['msg'] = 'j jump'
                logs.append(log_dict)

                j += 1
                continue

            if s + r <= t and j == v_m_l_i:
                log_dict['msg'] = 't bigger'
                logs.append(log_dict)

                n_ts.append(t)
                i += 1
                continue

        targets = n_ts

    log_table(logs, position='left')

    min_location = min(targets)
    print(f'min_location: {min_location}')


@profiler
def part_two():
    for line in get_lines(__file__):
        pass


clear_log()
part_one()
part_two()
