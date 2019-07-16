import React from 'react';
import EditorRunForm from '../editor/HGEditorRunForm';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Typography from '@material-ui/core/Typography';
import { withTheme, withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

const styles = theme => ({

    root: {
        flexGrow: 1,
    },
});

function TabContainer(props) {
    return (
        <Typography component="div" style={{ padding: 8 * 3 }}>
            {props.children}
        </Typography>
    );
}

class HGContainer extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            // checked: false,
            value: 0,
        }
        this.handleChange = this.handleChange.bind(this);
    }

    // handleChange(event, newCheckedValue) {
    //     this.setState({ checked: newCheckedValue });
    // }

    handleChange(event, newValue) {
        this.setState({ value: newValue });
    }

    render() {
        const { classes } = this.props;

        return (
            <TabContainer>
                {/* <FormControlLabel
                    control={
                        <Switch
                            checked={this.state.checked}
                            onChange={this.handleChange}
                            color="primary"
                        />
                    }
                    label="viz"
                /> */}
                <div className={classes.root}>
                    <Tabs
                        value={this.state.value}
                        onChange={this.handleChange}
                        indicatorColor="primary"
                        textColor="primary"
                        centered
                    >
                        <Tab label="Editor" />
                        <Tab label="Viz" />
                    </Tabs>
                </div>
                <TabContainer>
                {this.state.value == 0 && <EditorRunForm />}
                {this.state.value == 1 && <div> Visualization </div>}
                </TabContainer>
            </TabContainer>
        );
    }
}
export default withTheme(withStyles(styles)(HGContainer));