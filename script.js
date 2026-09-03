// ==========================================
// 1. DATA STRUCTURES & PRE-LOADED RECORDS
// ==========================================
const FACULTY_ACCOUNTS = { "admin": "teacher123", "ali": "ali1234" };

const STUDENT_DATABASE = {
    "101": {
        name: "Ali Ahmed",
        marks: { English: 82, Mathematics: 91, Computer: 88, Physics: 76, PakStudies: 75 },
        total: 412,
        pct: 82.4,
        grade: "A",
        status: "Pass"
    },
    "102": {
        name: "Ahmed Hassan",
        marks: { English: 65, Mathematics: 72, Computer: 80, Physics: 70, PakStudies: 71 },
        total: 358,
        pct: 71.6,
        grade: "B",
        status: "Pass"
    },
    "103": {
        name: "Sara Khan",
        marks: { English: 95, Mathematics: 92, Computer: 89, Physics: 90, PakStudies: 90 },
        total: 456,
        pct: 91.2,
        grade: "A+",
        status: "Pass"
    }
};

const loginContainer = document.getElementById("login-container");
const dashboardContainer = document.getElementById("dashboard-container");

// ==========================================
// 2. TAB NAVIGATION LOGIC
// ==========================================
function showSection(sectionId, btnElement) {
    document.querySelectorAll(".dashboard-section").forEach(sec => sec.classList.add("hidden"));
    document.getElementById(sectionId).classList.remove("hidden");

    if (btnElement) {
        document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));
        btnElement.classList.add("active");
    }

    if (sectionId === 'view-section') renderRoster();
    if (sectionId === 'stats-section') renderStatistics();
}

// ==========================================
// 3. AUTHENTICATION LOGIC
// ==========================================
document.getElementById("login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const usr = document.getElementById("username").value.trim().toLowerCase();
    const pwd = document.getElementById("password").value.trim();

    if (FACULTY_ACCOUNTS[usr] && FACULTY_ACCOUNTS[usr] === pwd) {
        loginContainer.classList.add("hidden");
        dashboardContainer.classList.remove("hidden");
        
        const rosterBtn = document.querySelectorAll('.nav-btn')[1];
        showSection('view-section', rosterBtn);
    } else {
        document.getElementById("login-error").innerText = " Incorrect Username or Password!";
    }
});

document.getElementById("logout-btn").addEventListener("click", () => {
    dashboardContainer.classList.add("hidden");
    loginContainer.classList.remove("hidden");
});

// ==========================================
// 4. METRIC CALCULATIONS
// ==========================================
function calculateMetrics(marks) {
    const total = Object.values(marks).reduce((a, b) => a + b, 0);
    const pct = Number(((total / 500) * 100).toFixed(2));
    let grade = "F";
    if (pct >= 90) grade = "A+";
    else if (pct >= 80) grade = "A";
    else if (pct >= 70) grade = "B";
    else if (pct >= 60) grade = "C";
    else if (pct >= 50) grade = "D";

    const hasFailedSub = Object.values(marks).some(m => m < 40);
    const status = (grade === "F" || hasFailedSub) ? "Fail" : "Pass";
    return { total, pct, grade, status };
}

// ==========================================
// 5. ADD STUDENT
// ==========================================
document.getElementById("add-student-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const roll = document.getElementById("add-roll").value.trim();
    const name = document.getElementById("add-name").value.trim();

    if (STUDENT_DATABASE[roll]) {
        return;
    }

    const marks = {
        English: parseFloat(document.getElementById("add-eng").value) || 0,
        Mathematics: parseFloat(document.getElementById("add-math").value) || 0,
        Computer: parseFloat(document.getElementById("add-comp").value) || 0,
        Physics: parseFloat(document.getElementById("add-phy").value) || 0,
        PakStudies: parseFloat(document.getElementById("add-pak").value) || 0
    };

    STUDENT_DATABASE[roll] = { name, marks, ...calculateMetrics(marks) };
    document.getElementById("add-student-form").reset();
    
    const rosterBtn = document.querySelectorAll('.nav-btn')[1];
    showSection('view-section', rosterBtn);
});

// ==========================================
// 6. VIEW RECORDS & DIRECT DELETE (NO POP-UP)
// ==========================================
function renderRoster() {
    const tbody = document.getElementById("table-body");
    tbody.innerHTML = "";
    const rolls = Object.keys(STUDENT_DATABASE);

    if (rolls.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: #94a3b8;">No student records found.</td></tr>`;
        return;
    }

    rolls.forEach(roll => {
        const s = STUDENT_DATABASE[roll];
        tbody.innerHTML += `
            <tr>
                <td><strong>${roll}</strong></td>
                <td>${s.name}</td>
                <td>${s.pct}%</td>
                <td><span style="color:#38bdf8; font-weight:700;">${s.grade}</span></td>
                <td><span class="${s.status === 'Pass' ? 'badge-pass' : 'badge-fail'}">${s.status}</span></td>
                <td><button onclick="deleteStudent('${roll}')" class="btn-danger">Delete</button></td>
            </tr>`;
    });
}

// Pop-up removed completely
function deleteStudent(roll) {
    delete STUDENT_DATABASE[roll];
    renderRoster();
}

// ==========================================
// 7. SEARCH & DIRECT JUMP
// ==========================================
function handleSearch() {
    const roll = document.getElementById("search-roll-input").value.trim();
    const out = document.getElementById("search-output");
    
    if (STUDENT_DATABASE[roll]) {
        const s = STUDENT_DATABASE[roll];
        out.innerHTML = `
            <p style="font-size: 1.1rem; margin-bottom: 15px;">
                <strong>Student Found:</strong> ${s.name} (Roll: ${roll})<br>
                <span style="color:#94a3b8;">Percentage:</span> ${s.pct}% | 
                <span style="color:#94a3b8;">Grade:</span> ${s.grade} | 
                <span class="${s.status === 'Pass' ? 'badge-pass' : 'badge-fail'}">${s.status}</span>
            </p>
            <button onclick="jumpToResultCard('${roll}')" class="btn">View Full Result Card</button>
        `;
    } else {
        out.innerHTML = `<p class="error-msg"> Student record not found!</p>`;
    }
}

function jumpToResultCard(roll) {
    const navBtns = document.querySelectorAll(".nav-btn");
    showSection('result-section', navBtns[4]);
    document.getElementById("result-roll-input").value = roll;
    generateResultCard();
}

// ==========================================
// 8. UPDATE MARKS
// ==========================================
let currentUpdateRoll = null;
function loadStudentForUpdate() {
    const roll = document.getElementById("update-roll-input").value.trim();
    if (!STUDENT_DATABASE[roll]) {
        return;
    }
    currentUpdateRoll = roll;
    const s = STUDENT_DATABASE[roll];
    document.getElementById("update-student-heading").innerText = `Editing Marks for: ${s.name} (Roll: ${roll})`;
    document.getElementById("up-eng").value = s.marks.English;
    document.getElementById("up-math").value = s.marks.Mathematics;
    document.getElementById("up-comp").value = s.marks.Computer;
    document.getElementById("up-phy").value = s.marks.Physics;
    document.getElementById("up-pak").value = s.marks.PakStudies;
    document.getElementById("update-form-container").classList.remove("hidden");
}

document.getElementById("update-marks-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const marks = {
        English: parseFloat(document.getElementById("up-eng").value) || 0,
        Mathematics: parseFloat(document.getElementById("up-math").value) || 0,
        Computer: parseFloat(document.getElementById("up-comp").value) || 0,
        Physics: parseFloat(document.getElementById("up-phy").value) || 0,
        PakStudies: parseFloat(document.getElementById("up-pak").value) || 0
    };
    STUDENT_DATABASE[currentUpdateRoll].marks = marks;
    Object.assign(STUDENT_DATABASE[currentUpdateRoll], calculateMetrics(marks));
    document.getElementById("update-form-container").classList.add("hidden");
    document.getElementById("update-roll-input").value = "";
    
    const rosterBtn = document.querySelectorAll('.nav-btn')[1];
    showSection('view-section', rosterBtn);
});

// ==========================================
// 9. RESULT CARD & STATS
// ==========================================
function generateResultCard() {
    const roll = document.getElementById("result-roll-input").value.trim();
    const out = document.getElementById("result-card-display");
    if (!STUDENT_DATABASE[roll]) {
        out.innerHTML = `<p class="error-msg"> Student Record Not Found!</p>`;
        return;
    }
    const s = STUDENT_DATABASE[roll];
    out.innerHTML = `
        <div class="transcript">
            <h4>ACADEMIC TRANSCRIPT</h4>
            <div style="margin: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom:10px;">
                <p><strong>Name:</strong> ${s.name}</p>
                <p><strong>Roll No:</strong> ${roll}</p>
            </div>
            <div style="margin-bottom: 15px;">
                ${Object.entries(s.marks).map(([sub, score]) => `
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="color:#cbd5e1;">${sub}:</span>
                        <strong>${score} / 100</strong>
                    </div>
                `).join("")}
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top:12px;">
                <p><strong>Total Score:</strong> ${s.total} / 500</p>
                <p><strong>Percentage:</strong> ${s.pct}%</p>
                <p><strong>Final Grade:</strong> <span style="color:#38bdf8;">${s.grade}</span></p>
                <p style="margin-top:8px;"><strong>Status:</strong> <span class="${s.status === 'Pass' ? 'badge-pass' : 'badge-fail'}">${s.status}</span></p>
            </div>
        </div>`;
}

function renderStatistics() {
    const out = document.getElementById("stats-output");
    const rolls = Object.keys(STUDENT_DATABASE);
    if (!rolls.length) {
        out.innerHTML = "<p style='color:#94a3b8;'>No student data available.</p>";
        return;
    }
    const avg = (rolls.reduce((sum, r) => sum + STUDENT_DATABASE[r].pct, 0) / rolls.length).toFixed(2);
    const passes = rolls.filter(r => STUDENT_DATABASE[r].status === "Pass").length;

    out.innerHTML = `
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px;">
            <div style="background:rgba(15, 23, 42, 0.6); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
                <h5 style="color:#94a3b8;">Total Students</h5>
                <p style="font-size:1.5rem; font-weight:bold; color:#38bdf8;">${rolls.length}</p>
            </div>
            <div style="background:rgba(15, 23, 42, 0.6); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
                <h5 style="color:#94a3b8;">Class Average</h5>
                <p style="font-size:1.5rem; font-weight:bold; color:#38bdf8;">${avg}%</p>
            </div>
            <div style="background:rgba(15, 23, 42, 0.6); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
                <h5 style="color:#94a3b8;">Passed</h5>
                <p style="font-size:1.5rem; font-weight:bold; color:#34d399;">${passes}</p>
            </div>
            <div style="background:rgba(15, 23, 42, 0.6); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.1);">
                <h5 style="color:#94a3b8;">Failed</h5>
                <p style="font-size:1.5rem; font-weight:bold; color:#f87171;">${rolls.length - passes}</p>
            </div>
        </div>`;
}