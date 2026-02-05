document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.querySelector('#task');
    const submit = document.querySelector('#Submit');
    const tasklist = document.querySelector('#tasks');
    const markDoneBtn = document.querySelector('#mark-done-btn');
    const deleteAllBtn = document.querySelector('#delete-all-btn');
    const totalTasksEl = document.querySelector('#total-tasks');
    const completedTasksEl = document.querySelector('#completed-tasks');
    const remainingTasksEl = document.querySelector('#remaining-tasks');
    const cheerQuote = document.querySelector('#cheer-quote');
    const progressBar = document.querySelector('#progress-bar');
    
    submit.disabled = true;

    taskInput.onkeyup = () => {
        if(taskInput.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    document.querySelector('form').onsubmit = () => {
        const task = taskInput.value.trim();
        if(!task){
            alert("Task cannot be empty!");
            return false;
        }
        
        addTask(task);
        taskInput.value = '';
        submit.disabled = true;
        return false;
    }

    function addTask(taskText) {
        const li = document.createElement('li');
        
        const taskContent = document.createElement('div');
        taskContent.className = 'task-content';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'task-checkbox';
        
        const taskTextEl = document.createElement('span');
        taskTextEl.className = 'task-text';
        taskTextEl.textContent = taskText;
        
        const del = document.createElement('button');
        del.className = 'delete-task-btn';
        del.innerHTML = '<i class="fa-regular fa-trash-can"></i>';
        del.onclick = (e) => {
            e.stopPropagation();
            li.remove();
            updateDashboard();
        };
        
        taskContent.appendChild(checkbox);
        taskContent.appendChild(taskTextEl);
        li.appendChild(taskContent);
        li.appendChild(del);
        tasklist.appendChild(li);
        
        updateDashboard();
    }

    markDoneBtn.onclick = () => {
        const tasks = tasklist.querySelectorAll('li');
        let markedCount = 0;
        
        tasks.forEach(task => {
            const checkbox = task.querySelector('.task-checkbox');
            if(checkbox && checkbox.checked && !task.classList.contains('completed')) {
                task.classList.add('completed');
                markedCount++;
            }
        });
        
        if(markedCount === 0) {
            alert("Please select tasks to mark as done!");
        }
        
        updateDashboard();
    };

    deleteAllBtn.onclick = () => {
        const tasks = tasklist.querySelectorAll('li');
        const checkedTasks = Array.from(tasks).filter(task => {
            const checkbox = task.querySelector('.task-checkbox');
            return checkbox && checkbox.checked;
        });
        
        if(checkedTasks.length === 0) {
            alert("Please select tasks to delete!");
            return;
        }
        
        if(confirm(`Are you sure you want to delete ${checkedTasks.length} selected task(s)?`)) {
            checkedTasks.forEach(task => task.remove());
            updateDashboard();
        }
    };

    function updateDashboard() {
        const allTasks = tasklist.querySelectorAll('li');
        const completedTasks = tasklist.querySelectorAll('li.completed');
        
        const total = allTasks.length;
        const completed = completedTasks.length;
        const remaining = total - completed;
        
        totalTasksEl.textContent = total;
        completedTasksEl.textContent = completed;
        remainingTasksEl.textContent = remaining;
        
        const progress = total > 0 ? (completed / total) * 100 : 0;
        progressBar.style.width = progress + '%';
        
        if(total > 0 && remaining === 0) {
            cheerQuote.classList.add('show');
        } else {
            cheerQuote.classList.remove('show');
        }
    }

    updateDashboard();
});