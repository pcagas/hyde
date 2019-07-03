import React from 'react';
import { withTheme, withStyles } from '@material-ui/core/styles';
import Fab from '@material-ui/core/Fab';
import NewFolderIcon from '@material-ui/icons/CreateNewFolderOutlined';

const styles = theme => ({
    fabmargin: {
        margin: 20
      }
    
    });

class CreateFromExample extends React.Component {

    constructor(props) {
        super(props)
        
      }

    render() {
        const {theme, classes } = this.props;  

        return (
            <Fab size="small" color="primary" aria-label="Add" className={classes.fabmargin}>
                <NewFolderIcon />
              </Fab>
        );
    }
}
export default withTheme(withStyles(styles)(CreateFromExample));