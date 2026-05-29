// Click counter
let clickCount = 0;
const myButton = document.getElementById('myButton');
const message = document.getElementById('message');
const counter = document.getElementById('counter');

// Button click handler
myButton.addEventListener('click', function() {
    clickCount++;
    counter.textContent = clickCount;

    // Show message
    message.textContent = `You clicked ${clickCount} time${clickCount !== 1 ? 's' : ''}!`;
    message.className = 'message success';

    // Animate button
    myButton.style.transform = 'scale(0.95)';
    setTimeout(() => {
        myButton.style.transform = 'scale(1)';
    }, 100);
});

// Todo list functionality
const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');

// Add todo
function addTodo() {
    const text = todoInput.value.trim();
    
    if (text === '') {
        message.textContent = 'Please enter a task!';
        message.className = 'message info';
        return;
    }

    const li = document.createElement('li');
    li.className = 'todo-item';
    
    const span = document.createElement('span');
    span.textContent = text;
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'todo-delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = function() {
        li.remove();
        updateMessage();
    };
    
    li.appendChild(span);
    li.appendChild(deleteBtn);
    
    // Click to complete
    span.style.cursor = 'pointer';
    span.addEventListener('click', function() {
        li.classList.toggle('completed');
    });
    
    todoList.appendChild(li);
    todoInput.value = '';
    updateMessage();
}

function updateMessage() {
    const count = todoList.children.length;
    if (count === 0) {
        message.textContent = 'No tasks yet. Add one!';
        message.className = 'message info';
    } else {
        message.textContent = `You have ${count} task${count !== 1 ? 's' : ''}`;
        message.className = 'message success';
    }
}

addBtn.addEventListener('click', addTodo);

// Add on Enter key
todoInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTodo();
    }
});

// Initialize
updateMessage();
