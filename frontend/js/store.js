// Gerenciador de estado simples (sem dependências externas)
class Store {
  constructor() {
    this.state = {
      user: null,
      isLoading: false,
      priceChanges: [],
      products: [],
      stores: [],
    };
    this.listeners = [];
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }

  notify() {
    this.listeners.forEach((listener) => listener(this.state));
  }

  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.notify();
  }

  getState() {
    return this.state;
  }

  // Actions
  setUser(user) {
    this.setState({ user });
  }

  setLoading(isLoading) {
    this.setState({ isLoading });
  }

  setPriceChanges(priceChanges) {
    this.setState({ priceChanges });
  }

  addPriceChange(priceChange) {
    const priceChanges = [priceChange, ...this.state.priceChanges];
    this.setState({ priceChanges });
  }

  updatePriceChange(id, updates) {
    const priceChanges = this.state.priceChanges.map((pc) =>
      pc.id === id ? { ...pc, ...updates } : pc,
    );
    this.setState({ priceChanges });
  }

  removePriceChange(id) {
    const priceChanges = this.state.priceChanges.filter((pc) => pc.id !== id);
    this.setState({ priceChanges });
  }

  setProducts(products) {
    this.setState({ products });
  }

  setStores(stores) {
    this.setState({ stores });
  }

  logout() {
    this.setState({
      user: null,
      priceChanges: [],
      products: [],
      stores: [],
    });
  }
}

// Instância global
const store = new Store();
