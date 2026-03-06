document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('url-input');
    const audioOnly = document.getElementById('audio-only');
    const downloadBtn = document.getElementById('download-btn');
    const statusContainer = document.getElementById('status-container');
    const resultContainer = document.getElementById('result-container');
    const resetBtn = document.getElementById('reset-btn');
    const statusMessage = document.getElementById('status-message');

    downloadBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        
        if (!url) {
            alert('URL을 입력해주세요!');
            return;
        }

        // UI 상태 전환: 로딩 중
        downloadBtn.disabled = true;
        statusContainer.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        statusMessage.textContent = '서버에서 미디어를 분석 및 추출 중입니다. 잠시만 기다려주세요...';

        try {
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    is_audio_only: audioOnly.checked
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || '다운로드 중 오류가 발생했습니다.');
            }

            // 파일 다운로드 처리
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            
            // 헤더에서 파일명 추출 시도 (없으면 기본값)
            const contentDisposition = response.headers.get('Content-Disposition');
            let fileName = audioOnly.checked ? 'extracted_audio.mp3' : 'extracted_video.mp4';
            
            if (contentDisposition && contentDisposition.indexOf('filename=') !== -1) {
                fileName = contentDisposition.split('filename=')[1].replace(/"/g, '');
            }

            a.href = downloadUrl;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
            a.remove();

            // UI 상태 전환: 성공
            statusContainer.classList.add('hidden');
            resultContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            alert('오류: ' + error.message);
            statusContainer.classList.add('hidden');
        } finally {
            downloadBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        urlInput.value = '';
        resultContainer.classList.add('hidden');
        statusContainer.classList.add('hidden');
    });
});
