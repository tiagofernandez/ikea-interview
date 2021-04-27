import axios from "axios";

const api = {
    getProducts: async () => {
        const res = await axios.get("/api/products");
        return res.data?.products || [];
    },
    sellProduct: async (name) => {
        const res = await axios.delete("/api/products", { data: { name } });
        return res.data;
    },
    upload: async (path, data) => {
        const res = await axios.post(`/api/${path}`, data);
        return res.data;
    },
};

export default api;
