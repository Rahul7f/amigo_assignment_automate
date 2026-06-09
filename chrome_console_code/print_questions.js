let output = '';

document.querySelectorAll('.que').forEach((q, i) => {
    const question =
        q.querySelector('.qtext')?.innerText.trim() || '';

    output += `Question Number: Question ${i + 1}\n`;
    output += `Question Text: ${question}\n`;
    output += `Options:\n`;

    const answerArea = q.querySelector('.answer');

    if (answerArea) {
        output += answerArea.innerText.trim() + '\n';
    }

    output += '\n---------------------------------\n\n';
});

copy(output);
console.log('Copied to clipboard');