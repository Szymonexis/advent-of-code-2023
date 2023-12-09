from typing import List, Tuple, TypedDict
from utils import clear_log, get_lines, log, log_table, profiler


class Vector(TypedDict):
    d: int
    s: int
    r: int
    o: int


VectorMap = Tuple[str, List[Vector]]


class SeedsAndVectorMaps(TypedDict):
    seeds: list[int]
    vector_maps: list[VectorMap]


def get_seeds(line: str) -> list[int]:
    return list(map(int, map(str.strip, line.split(':')[1].strip().split(' '))))


def get_map(lines: list[str], name: str) -> VectorMap:
    vectors: list[Vector] = []
    for line in lines:
        [d, s, r] = list(map(int, map(str.strip, line.strip().split(' '))))
        vectors.append(Vector(d=d, s=s, r=r, o=d-s))

    return (name, sorted(vectors, key=lambda x: x['s']))


def get_seeds_and_vector_maps() -> SeedsAndVectorMaps:
    lines = get_lines(__file__)
    seeds = sorted(get_seeds(lines[0]))

    section_indexes = []
    off = 3
    for i in range(off, len(lines[off:])):
        if lines[i] == '':
            section_indexes.append(i)
    section_indexes.append(len(lines))

    vector_maps: list[VectorMap] = []
    start = 1
    for section_index in section_indexes:
        map_lines = lines[start + 2:section_index]
        vector_maps.append(get_map(map_lines, lines[start + 1]))
        start = section_index

    return SeedsAndVectorMaps(seeds=seeds, vector_maps=vector_maps)


@profiler
def part_one():
    m = get_seeds_and_vector_maps()
    seeds = m['seeds']
    vector_maps = m['vector_maps']
    targets = seeds
    for (name, vectors) in vector_maps:
        i = 0
        j = 0
        n_ts = []
        vul = len(vectors) - 1
        while i < len(targets):
            v = vectors[j]
            d = v['d']
            s = v['s']
            o = v['o']
            r = v['r']
            e = s + r
            t = targets[i]

            t_smaller_than_v = t < s
            t_in_range_v = s <= t and t < e
            t_bigger_than_v = e <= t

            if t_smaller_than_v:
                n_ts.append(t)
                i += 1
                continue

            if t_in_range_v:
                n_ts.append(t + o)
                i += 1
                continue

            if t_bigger_than_v:
                if j < vul:
                    j += 1
                    continue

                if j == vul:
                    n_ts.append(t)
                    i += 1
                    continue

        targets = sorted(n_ts)

    min_location = min(targets)
    print(f'min_location: {min_location}')


class SeedRangesAndVectorMaps(TypedDict):
    seed_ranges: list[tuple[int, int]]
    vector_maps: list[VectorMap]


def get_seed_ranges(line: str) -> list[tuple[int, int]]:
    seeds = get_seeds(line)

    seed_ranges: list[tuple[int, int]] = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append((seeds[i], seeds[i+1]))

    return seed_ranges


def get_seed_ranges_and_vector_maps() -> SeedRangesAndVectorMaps:
    lines = get_lines(__file__)
    seed_ranges = get_seed_ranges(lines[0])

    section_indexes = []
    off = 3
    for i in range(off, len(lines[off:])):
        if lines[i] == '':
            section_indexes.append(i)
    section_indexes.append(len(lines))

    vector_maps: list[VectorMap] = []
    start = 1
    for section_index in section_indexes:
        map_lines = lines[start + 2:section_index]
        vector_maps.append(get_map(map_lines, lines[start + 1]))
        start = section_index

    return SeedsAndVectorMaps(seed_ranges=seed_ranges, vector_maps=vector_maps)


@profiler
def part_two():
    m = get_seed_ranges_and_vector_maps()
    seed_ranges = m['seed_ranges']
    vector_maps = m['vector_maps']

    print(seed_ranges)


part_one()
part_two()
