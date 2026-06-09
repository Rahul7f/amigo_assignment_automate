const questions = document.querySelectorAll('.que');

questions.forEach((q, index) => {
    const questionText =
        q.querySelector('.qtext')?.innerText.trim() ||
        'Question text not found';

    const options = [...q.querySelectorAll('label')].map(
        x => x.innerText.trim()
    );

    console.log(`Question Number: Question ${index + 1}`);
    console.log(`Question Text: ${questionText}`);
    console.log('Options:');

    options.forEach(opt => {
        console.log(opt);
    });

    console.log('-----------------------------------');
});