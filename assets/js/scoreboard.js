/**
 * CTFd-Paihangb 排行榜 JavaScript
 */

(function() {
    'use strict';

    // 当前状态
    let currentTrack = 'all';
    let currentSchool = 'all';
    let searchQuery = '';
    let allData = [];

    // DOM 元素
    const scoreboardBody = document.getElementById('scoreboardBody');
    const trackButtons = document.querySelectorAll('.track-btn');
    const schoolFilter = document.getElementById('schoolFilter');
    const searchInput = document.getElementById('searchInput');
    const resetFilterBtn = document.getElementById('resetFilter');
    const currentTrackSpan = document.getElementById('currentTrack');
    const currentSchoolSpan = document.getElementById('currentSchool');
    const teamCountSpan = document.getElementById('teamCount');
    const emptyState = document.getElementById('emptyState');
    const scoreboardTable = document.getElementById('scoreboardTable');

    /**
     * 初始化
     */
    function init() {
        // 绑定赛道切换按钮
        trackButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                const track = this.dataset.track;
                switchTrack(track);
            });
        });

        // 绑定学校筛选
        if (schoolFilter) {
            schoolFilter.addEventListener('change', function() {
                currentSchool = this.value;
                loadScoreboard();
            });
        }

        // 绑定搜索框
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                searchQuery = this.value.toLowerCase();
                filterData();
            });
        }

        // 绑定重置按钮
        if (resetFilterBtn) {
            resetFilterBtn.addEventListener('click', resetFilters);
        }

        // 加载初始数据
        loadScoreboard();

        // 自动刷新（每30秒）
        setInterval(loadScoreboard, 30000);
    }

    /**
     * 切换赛道
     */
    function switchTrack(track) {
        currentTrack = track;

        // 更新按钮状态
        trackButtons.forEach(btn => {
            if (btn.dataset.track === track) {
                btn.classList.remove('btn-outline-primary');
                btn.classList.add('btn-primary', 'active');
            } else {
                btn.classList.remove('btn-primary', 'active');
                btn.classList.add('btn-outline-primary');
            }
        });

        // 加载数据
        loadScoreboard();
    }

    /**
     * 加载排行榜数据
     */
    function loadScoreboard() {
        showLoading();

        const params = new URLSearchParams();
        if (currentTrack !== 'all') {
            params.append('track', currentTrack);
        }
        if (currentSchool !== 'all') {
            params.append('school', currentSchool);
        }

        fetch(`/api/scoreboard/data?${params.toString()}`)
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    allData = result.data;
                    filterData();
                    updateInfo();
                } else {
                    showError('加载失败');
                }
            })
            .catch(error => {
                console.error('Error loading scoreboard:', error);
                showError('加载失败，请刷新页面重试');
            });
    }

    /**
     * 过滤数据（本地搜索）
     */
    function filterData() {
        let filteredData = allData;

        // 搜索过滤
        if (searchQuery) {
            filteredData = filteredData.filter(team => 
                team.team_name.toLowerCase().includes(searchQuery)
            );
        }

        // 显示数据
        renderScoreboard(filteredData);
    }

    /**
     * 渲染排行榜
     */
    function renderScoreboard(data) {
        if (!data || data.length === 0) {
            showEmpty();
            return;
        }

        scoreboardTable.style.display = 'table';
        emptyState.style.display = 'none';

        let html = '';
        data.forEach((team, index) => {
            const rank = index + 1;
            const rankClass = rank <= 3 ? `rank-${rank}` : 'rank-other';
            
            html += `
                <tr>
                    <td class="text-center">
                        <span class="rank-badge ${rankClass}">${rank}</span>
                    </td>
                    <td>
                        <a href="/teams/${team.team_id}" class="team-link">
                            ${escapeHtml(team.team_name)}
                        </a>
                    </td>
                    <td class="text-center">
                        <span class="school-name">${escapeHtml(team.school)}</span>
                    </td>
                    <td class="text-center">
                        <span class="badge track-badge track-${team.track}">${escapeHtml(team.track)}</span>
                    </td>
                    <td class="text-center solve-count">${team.solve_count}</td>
                    <td class="text-center score-cell">${team.score}</td>
                </tr>
            `;
        });

        scoreboardBody.innerHTML = html;
        teamCountSpan.textContent = data.length;
    }

    /**
     * 显示加载状态
     */
    function showLoading() {
        scoreboardTable.style.display = 'table';
        emptyState.style.display = 'none';
        scoreboardBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                    <p class="mt-2">加载中...</p>
                </td>
            </tr>
        `;
    }

    /**
     * 显示空状态
     */
    function showEmpty() {
        scoreboardTable.style.display = 'none';
        emptyState.style.display = 'block';
        teamCountSpan.textContent = '0';
    }

    /**
     * 显示错误
     */
    function showError(message) {
        scoreboardTable.style.display = 'table';
        emptyState.style.display = 'none';
        scoreboardBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-danger py-5">
                    <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                    <p>${message}</p>
                </td>
            </tr>
        `;
    }

    /**
     * 更新信息显示
     */
    function updateInfo() {
        // 更新当前赛道显示
        const trackNames = {
            'all': '总榜',
            '新生赛道': '新生榜',
            '进阶赛道': '进阶榜',
            '社会赛道': '社会榜'
        };
        currentTrackSpan.textContent = trackNames[currentTrack] || currentTrack;

        // 更新学校筛选显示
        if (currentSchool !== 'all') {
            currentSchoolSpan.innerHTML = ` | 学校：<span class="font-weight-bold">${escapeHtml(currentSchool)}</span>`;
        } else {
            currentSchoolSpan.innerHTML = '';
        }
    }

    /**
     * 重置筛选器
     */
    function resetFilters() {
        currentSchool = 'all';
        searchQuery = '';
        
        if (schoolFilter) {
            schoolFilter.value = 'all';
        }
        if (searchInput) {
            searchInput.value = '';
        }

        loadScoreboard();
    }

    /**
     * HTML 转义
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

