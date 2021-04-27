export function reducer(state, action) {
    switch (action.type) {
        case "refresh-products": {
            const { products } = action;
            return {
                ...state,
                products,
            };
        }
        default: {
            return state;
        }
    }
}
