// establish the socket connection
var socket = io.connect('http://' + document.domain + ':' + location.port);
// define the board and the constants
let board = [["", "", ""], ["", "", ""], ["", "", ""]]
const player = "X";
const computer = "O";

const addMove = (i, j) => {
    // activate overlay to prevent multiple clicks
    document.getElementById('overlay').style.display = 'block';
    // add the user to the board
    socket.emit('action', {'board': board, 'move': [i, j]});
    // get ai move after short delay to make the user move has been registered
    setTimeout(function(){ socket.emit('get_ai_move', board); }, 10);
    // remove overlay after the ai move has been added
    setTimeout(function() { document.getElementById('overlay').style.display = 'none'; }, 500)
};

const reset_board = () => {
    socket.emit("reset")
    document.querySelector("#result").textContent = "";
};



document.addEventListener('DOMContentLoaded', () => {
   
    window.onload = function(){
        const board_container = document.querySelector(".play-area");

        const render_board = () => {
            board_container.innerHTML = "";
            // fill up the play area with the cells of the board
            board.forEach((row, i) => {
                row.forEach((col, j) => {
                    board_container.innerHTML += `<div id="block_${i}${j}" class="block" onclick="addMove(${i}, ${j})">${board[i][j]}</div>`;
                    // assign color according to symbol (X or O)
                    if (col == player) {
                        document.querySelector(`#block_${i}${j}`).classList.add("text-info");
                    }
                    else if (col == computer) {
                        document.querySelector(`#block_${i}${j}`).classList.add("text-primary");
                    }

                    if (col == player || col == computer) {
                        // document.querySelector(`#block_${i}${j}`).classList.add("occupied");
                        document.querySelector(`#block_${i}${j}`).removeAttribute('onclick');
                      }
                });
            });
        };

        render_board();

        socket.on("update", state => {
            // check if game is over
            socket.emit("check_status", state);
            board = state;
            render_board();
            
        });
        socket.on("game_over", result => {
            // display the result of the game
            let resultArea = document.querySelector('#result');
            if (result == 'winner: X') {
                resultArea.classList.add('text-success');
            }
            else if (result == 'winner: O') {
                resultArea.classList.add('text-warning');
            }
            else {
                resultArea.classList.add('text-secondary')
            }
            resultArea.textContent = result

            // remove the onclick attributes for the blocks to stop the game
            blocks = document.querySelectorAll(".block");
            blocks.forEach(block => {
                block.removeAttribute('onclick');
            });
        });
    };
});