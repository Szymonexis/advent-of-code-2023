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


@profiler
def part_two():
    # get data
    seeds: list[tuple[int, int]] = []
    maps: dict[str, list[tuple[int, int, int]]] = {}

    name = ''
    for line in filter(lambda x: x != '', get_lines(__file__)):
        if line.find('seeds:') != -1:
            temp_seeds = list(map(int, line.split(':')[1].strip().split(' ')))
            seeds = [(temp_seeds[i], temp_seeds[i+1])
                     for i in range(0, len(temp_seeds), 2)]
        elif line.find(':') != -1:
            name = line.split(' ')[0]
            maps[name] = []
        else:
            maps[name].append(tuple(map(int, line.split(' '))))

    # map the data over every map
    targets: list[tuple[int, int, str]] = [
        (seed[0], seed[1], '') for seed in seeds]
    for (map_name, map_values) in maps.items():
        for map_value in map_values:
            next_targets: list[tuple[int, int, str]] = []
            for target in targets:
                (d, s, r) = map_value
                (t_s, t_r, name) = target
                o = d - s
                e = s + r - 1
                t_e = t_s + t_r - 1

                if name == map_name:
                    next_targets.append(target)
                    continue

                # out of range
                if t_e < s or t_s > e:
                    next_targets.append((t_s, t_r, ''))
                    continue

                # fully in range
                if t_s >= s and t_e <= e:
                    next_targets.append((t_s + o, t_r, map_name))
                    continue

                # left out, right in range
                if t_s < s and t_e <= e:
                    left_range = s - t_s
                    right_range = t_r - left_range

                    next_targets.append((t_s, left_range, ''))
                    next_targets.append((s + o, right_range, map_name))
                    continue

                # left in range, right out
                if t_s >= s and t_e > e:
                    left_range = e - t_s
                    right_range = t_r - left_range

                    next_targets.append((t_s + o, left_range, map_name))
                    next_targets.append((e + 1, right_range, ''))
                    continue

                # left out, center in range, right out
                if t_s < s and t_e > e:
                    left_range = s - t_s
                    center_range = r
                    right_range = t_r - left_range - center_range

                    next_targets.append((t_s, left_range, ''))
                    next_targets.append((s + o, center_range, map_name))
                    next_targets.append((e + 1, right_range, ''))
                    continue

            targets = next_targets

    min_location = min(targets, key=lambda x: x[0])
    print(f'min_location: {min_location[0]}')


part_one()
part_two()
