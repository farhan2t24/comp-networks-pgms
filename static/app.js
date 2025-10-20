document.getElementById('sendBtn').addEventListener('click', async () => {
  const message = document.getElementById('message').value;
  if (!message) return alert('enter a message');
  try {
    const res = await axios.post('/send', { message });
    document.getElementById('resultPlain').textContent = `Plaintext: ${message}`;
    document.getElementById('resultCipher').textContent = `Ciphertext: ${res.data.ciphertext}\nID: ${res.data.id}`;
    document.getElementById('msgId').value = res.data.id;
  } catch (err) {
    alert('error sending: ' + (err.response?.data?.error || err.message));
  }
});

document.getElementById('viewBtn').addEventListener('click', async () => {
  const id = document.getElementById('msgId').value;
  if (!id) return alert('paste id');
  try {
    const res = await axios.get(`/message/${id}`);
    document.getElementById('decrypted').textContent = res.data.message;
  } catch (err) {
    alert('error fetching: ' + (err.response?.status || err.message));
  }
});

document.getElementById('viewRawBtn').addEventListener('click', async () => {
  const id = document.getElementById('msgId').value;
  if (!id) return alert('paste id');
  if (!confirm('Show encrypted ciphertext?')) return;
  try {
    const res = await axios.get(`/raw/${id}`);
    document.getElementById('encrypted').textContent = `Ciphertext: ${res.data.ciphertext}\nIV: ${res.data.iv}`;
  } catch (err) {
    alert('error fetching raw: ' + (err.response?.status || err.message));
  }
});
