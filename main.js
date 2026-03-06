document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('url-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const audioOnly = document.getElementById('audio-only');
    const downloadBtn = document.getElementById('download-btn');
    const statusContainer = document.getElementById('status-container');
    const resultContainer = document.getElementById('result-container');
    const statusMessage = document.getElementById('status-message');
    const mediaInfoContainer = document.getElementById('media-info-container');
    const mediaThumbnail = document.getElementById('media-thumbnail');
    const mediaTitle = document.getElementById('media-title');
    const mediaDuration = document.getElementById('media-duration');
    const qualityList = document.getElementById('quality-list');

    let selectedFormatId = null;

    analyzeBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) { alert('URL을 입력해주세요!'); return; }

        console.log("분석 시작:", url);
        analyzeBtn.disabled = true;
        statusContainer.classList.remove('hidden');
        statusMessage.textContent = '미디어 정보를 분석 중입니다...';
        mediaInfoContainer.classList.add('hidden');

        try {
            const response = await fetch('/api/info', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            if (!response.ok) throw new Error('정보를 가져오는데 실패했습니다.');

            const data = await response.json();
            console.log("분석 결과:", data);

            mediaTitle.textContent = data.title;
            mediaThumbnail.src = data.thumbnail;
            mediaDuration.textContent = `길이: ${Math.floor(data.duration / 60)}분 ${data.duration % 60}초`;
            
            qualityList.innerHTML = '';
            data.formats.forEach(f => {
                const item = document.createElement('div');
                item.className = 'quality-item';
                item.textContent = f.resolution;
                item.onclick = () => {
                    document.querySelectorAll('.quality-item').forEach(el => el.classList.remove('selected'));
                    item.classList.add('selected');
                    selectedFormatId = f.format_id;
                };
                qualityList.appendChild(item);
            });

            if (data.formats.length > 0) qualityList.firstChild.click();

            mediaInfoContainer.classList.remove('hidden');
            statusContainer.classList.add('hidden');
        } catch (error) {
            alert('에러: ' + error.message);
            statusContainer.classList.add('hidden');
        } finally {
            analyzeBtn.disabled = false;
        }
    });

    downloadBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return;

        downloadBtn.disabled = true;
        statusContainer.classList.remove('hidden');
        statusMessage.textContent = '다운로드 중입니다...';

        try {
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    url,
                    is_audio_only: audioOnly.checked,
                    format_id: selectedFormatId
                })
            });

            if (!response.ok) throw new Error('다운로드 실패');

            const blob = await response.blob();
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = audioOnly.checked ? 'audio.mp3' : 'video.mp4';
            a.click();

            statusContainer.classList.add('hidden');
            resultContainer.classList.remove('hidden');
        } catch (error) {
            alert('에러: ' + error.message);
            statusContainer.classList.add('hidden');
        } finally {
            downloadBtn.disabled = false;
        }
    });
});
