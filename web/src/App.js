import AppBar from "@material-ui/core/AppBar";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import React from "react";

import api from "./api";
import AppContext from "./AppContext";
import ActionsView from "./components/ActionsView";
import ProductsView from "./components/ProductsView";
import logo from "./logo.png";
import { reducer } from "./store";

const useStyles = makeStyles((t) => ({
    container: {
        padding: t.spacing(3),
    },
    root: {
        flexGrow: 1,
    },
    logo: {
        width: 50,
    },
    title: {
        flexGrow: 1,
    },
}));

export default function App() {
    const classes = useStyles();

    const [state, dispatch] = React.useReducer(reducer, { products: [] });
    const [context, setContext] = React.useState(null);

    React.useEffect(() => {
        setContext({
            dispatch,
        });
    }, [dispatch]);

    const refreshProducts = async () => {
        const products = await api.getProducts();
        dispatch({ type: "refresh-products", products });
    };
    React.useEffect(() => {
        refreshProducts();
    }, []);

    return context ? (
        <AppContext.Provider value={context}>
            <CssBaseline />
            <div className={classes.root}>
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6" className={classes.title}>
                            Warehouse
                        </Typography>
                        <img src={logo} className={classes.logo} alt="Logo" />
                    </Toolbar>
                </AppBar>
                <Container className={classes.container} maxWidth="xl">
                    <Grid container direction="column" spacing={3}>
                        <Grid item>
                            <ActionsView />
                        </Grid>
                        <Grid item>
                            <ProductsView products={state.products} onSell={refreshProducts} />
                        </Grid>
                    </Grid>
                </Container>
            </div>
        </AppContext.Provider>
    ) : (
        <span />
    );
}
