import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import React from "react";

import api from "../api";

const useStyles = makeStyles((t) => ({
    table: {
        minWidth: 650,
    },
}));

export default function ProductsView({ products, onSell, onError }) {
    const classes = useStyles();

    return products?.length > 0 ? (
        <Grid container direction="column" spacing={3}>
            <Grid item>
                <TableContainer component={Paper}>
                    <Table className={classes.table} aria-label="products table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Name</TableCell>
                                <TableCell>Quantity</TableCell>
                                <TableCell>Actions</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {products.map((p) => (
                                <TableRow key={p.name}>
                                    <TableCell component="th" scope="row">
                                        {p.name}
                                    </TableCell>
                                    <TableCell>{p.quantity}</TableCell>
                                    <TableCell>
                                        <Button
                                            disabled={p.quantity <= 0}
                                            variant="outlined"
                                            onClick={async () => {
                                                try {
                                                    await api.sellProduct(p.name);

                                                    if (onSell) {
                                                        onSell(p.name);
                                                    }
                                                } catch (err) {
                                                    if (onError) {
                                                        onError(err);
                                                    }
                                                }
                                            }}
                                        >
                                            Sell Unity
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Grid>
        </Grid>
    ) : (
        <span />
    );
}
