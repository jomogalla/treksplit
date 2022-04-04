class RecentlyVisited  {
    constructor(storageName) {
        this.storageName = storageName || 'recentlyVisited';

        const visited = JSON.parse(window.localStorage.getItem(storageName)) || {};

        this.visited = visited;
    }

    get visitedd() {
        return this.visited;
    }

    addVisit(hash, name) {
        this.visited[hash] = name;
        window.localStorage.setItem(this.storageName, JSON.stringify(this.visited));
    }
}

const recentlyVisited = new RecentlyVisited('recentlyVisited');