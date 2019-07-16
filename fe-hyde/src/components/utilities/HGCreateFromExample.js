import React from 'react';
import { withTheme, withStyles } from '@material-ui/core/styles';
import Fab from '@material-ui/core/Fab';
import NewFolderIcon from '@material-ui/icons/CreateNewFolderOutlined';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import IconButton from '@material-ui/core/IconButton';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';

const styles = theme => ({
  fabmargin: {
    margin: 20
  }

});

class CreateFromExample extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      anchorEl: null,
      auth: true,
      open: false,
      value: "",
      inputFiles: [],
    }

    this.handleClose = this.handleClose.bind(this);
    this.handleMenu = this.handleMenu.bind(this);
    this.handleDialogClose = this.handleDialogClose.bind(this);
    this.handleDialogOpen = this.handleDialogOpen.bind(this);
    this.handleDialogSubmit = this.handleDialogSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);

  }

  componentDidMount() {
    fetch(`http://localhost:3000/api/sims/exampleSims`)
      .then(response => response.json())
      .then(data => this.setState({ inputFiles: data.sims }));
  }

  handleClose() {
    this.setState({ anchorEl: null });
  }

  handleMenu(event) {
    this.setState({ anchorEl: event.currentTarget });
  }
  handleDialogClose() {
    this.setState({ open: false });
  }

  handleDialogOpen() {
    this.setState({ anchorEl: null });
    this.setState({ open: true });
  }

  handleDialogSubmit() {
    this.setState({ open: false });
    this.props.onClickCreateFromExampleButton && this.props.onClickCreateFromExampleButton({ 'name': this.state.value });
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  render() {
    const { theme, classes } = this.props;
    const open = Boolean(this.state.anchorEl);
    const { handleClose, handleMenu, handleDialogOpen } = this;
    const { anchorEl } = this.state

    return (

      // {auth && (
      <div>
        <IconButton
          onClick={handleMenu}
        >
          <Fab size="small" color="primary" aria-label="Add" className={classes.fabmargin}>
            <NewFolderIcon />
          </Fab>
        </IconButton>
        <Menu
          id="menu-example"
          anchorEl={anchorEl}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          keepMounted
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          open={open}
          onClose={handleClose}
        >
          {/* <MenuItem onClick={handleDialogOpen}>input_file1.lua</MenuItem>
          <MenuItem onClick={handleDialogOpen}>input_file2.lua</MenuItem>
          <MenuItem onClick={handleDialogOpen}>input_file3.lua</MenuItem> */}

          {this.state.inputFiles.map(row => (
            <MenuItem button key={row.id}
              onClick={() => handleDialogOpen(row)}
            >
              {row.name}
            </MenuItem>
          ))}

        </Menu>
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
      // )}




    );
  }
}
export default withTheme(withStyles(styles)(CreateFromExample));