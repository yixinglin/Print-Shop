
export const saveToLocalStorage = (key, object) => {
    localStorage.setItem(key, JSON.stringify(object));
}

export const restoreFromLocalStorage = (key) => {
    const item = localStorage.getItem(key);
    return item? JSON.parse(item) : null;
}