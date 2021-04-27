import Grid from "@material-ui/core/Grid";
import React from "react";

import api from "../api";
import AppContext from "../AppContext";
import UploadButton from "./UploadButton";

export default function ActionsView() {
    const { dispatch } = React.useContext(AppContext);

    const refreshProducts = async () => {
        const products = await api.getProducts();
        dispatch({ type: "refresh-products", products });
    };
    return (
        <Grid container spacing={3}>
            <Grid item>
                <UploadButton target="inventory" onSuccess={refreshProducts} />
            </Grid>
            <Grid item>
                <UploadButton target="products" onSuccess={refreshProducts} />
            </Grid>
        </Grid>
    );
}
