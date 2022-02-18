import operator

from trains.models import Train


def dfs_paths(graph, start, finish):
    """Функция поиска всех возможных маршрутов из
    одного города в другой. Вариант посещения одного
    и того же города 2 раза не рассматривается"""

    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == finish:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)

    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    qs = Train.objects.all().select_related('from_city', 'to_city')
    # qs = Train.objects.all()
    graph = get_graph(qs)
    data = form.cleaned_data

    from_city = data['from_city']
    to_city = data['to_city']
    travelling_time = data['travelling_time']
    cities = data['cities']

    found_routes = list(dfs_paths(graph, from_city.id, to_city.id))

    if not len(found_routes):
        raise ValueError('Маршрут, удовлетворяющий условиям поиска, не найден')
    if cities:
        _cities_id = [city.id for city in cities]
        right_routes = []
        for route in found_routes:
            if all(city_id in route for city_id in _cities_id):
                right_routes.append(route)
        if not right_routes:
            raise ValueError('Маршрут, проходящий через указанные города, не найден')
    else:
        right_routes = found_routes
    right_time_routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for route in right_routes:
        tmp = {'trains': []}
        total_time = 0
        for i in range(len(route) - 1):
            qs = all_trains[(route[i], route[i + 1])]
            q = qs[0]
            total_time += q.travel_time
            tmp['trains'].append(q)
        tmp['total_time'] = total_time

        if total_time <= travelling_time:
            right_time_routes.append(tmp)

    if not right_time_routes:
        raise ValueError('Время в пути по найденным маршрутам больше заданного')
    else:
        right_time_routes.sort(key=operator.itemgetter('total_time'))

    context['routes'] = right_time_routes
    context['cities'] = {'from_city': from_city.name, 'to_city': to_city.name}

    return context
