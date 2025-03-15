document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('encryptionForm').addEventListener('submit', async function (e) {
        e.preventDefault(); // Ngăn chặn hành vi submit mặc định

        const form = e.target;
        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const result = await response.json();
            const alertMessage = document.getElementById('alertMessage');

            if (result.success) {
                alertMessage.textContent = result.message;
                alertMessage.className = 'alert alert-success';
                alertMessage.classList.remove('d-none');
            } else {
                alertMessage.textContent = result.message;
                alertMessage.className = 'alert alert-danger';
                alertMessage.classList.remove('d-none');
            }
        } catch (error) {
            const alertMessage = document.getElementById('alertMessage');
            alertMessage.textContent = 'Đã xảy ra lỗi khi gửi yêu cầu.';
            alertMessage.className = 'alert alert-danger';
            alertMessage.classList.remove('d-none');
            console.error('Lỗi:', error);
        }
    });
});

