import React from 'react';
import { withTheme, withStyles } from '@material-ui/core/styles';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

const styles = theme => ({
  fabmargin: {
    margin: 20
  }

});

class CreateFromNew extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      open: false,
      value: "",
    }

    this.handleDialogClose = this.handleDialogClose.bind(this);
    this.handleDialogOpen = this.handleDialogOpen.bind(this);
    this.handleDialogSubmit = this.handleDialogSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);

  }

  handleDialogClose() {
    this.setState({ open: false });
  }

  handleDialogOpen() {
    this.setState({ open: true });
  }
  
  handleDialogSubmit() {
    this.setState({open: false});
    this.props.onClickCreateFromNewButton && this.props.onClickCreateFromNewButton({'name': this.state.value});
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  render() {

    const { theme, classes } = this.props;

    return (
      <div>
        <IconButton
          onClick={this.handleDialogOpen}
        >
          <Fab size="small" color="primary" aria-label="Add" className={classes.fabmargin}>
            <AddIcon />
          </Fab>
        </IconButton>
        <Dialog open={this.state.open} onClose={this.handleDialogClose} aria-labelledby="form-dialog-title">
          <DialogTitle id="form-dialog-title">Sim name required</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Please provide a name for your simulation.
        </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="simname"
              label="Sim Name"
              type="text"
              value={this.state.value}
              onChange={this.handleChange}
              fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleDialogClose} color="primary">
              Cancel
        </Button>
            <Button onClick={this.handleDialogSubmit} color="primary">
              Submit
        </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}
export default withTheme(withStyles(styles)(CreateFromNew));