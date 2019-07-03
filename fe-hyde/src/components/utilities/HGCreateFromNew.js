import React from 'react';
import { withTheme, withStyles } from '@material-ui/core/styles';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';

const styles = theme => ({
    fabmargin: {
        margin: 20
      }
    
    });

class CreateFromNew extends React.Component {

    constructor(props) {
        super(props)
        
      }

    render() {

        const {theme, classes } = this.props;  

        return (
            <Fab size="small" color="primary" aria-label="Add" className={classes.fabmargin}>
                <AddIcon />
              </Fab>
        );
    }
}
export default withTheme(withStyles(styles)(CreateFromNew));