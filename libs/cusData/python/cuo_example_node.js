/**
 * TestData 간단한 사용 예제 (Node.js)
 */

const { TestData } = require('./testdata');

function main() {
    console.log('TestData 간단한 사용 예제 (Node.js)\n');

    // 생성할 모든 객체를 추적 (메모리 정리용)
    const allObjects = [];

    try {
        // 예제 1: 기본 생성 및 설정
        console.log('='.repeat(50));
        console.log('예제 1: 기본 생성 및 설정');
        console.log('='.repeat(50));

        const person = new TestData();
        allObjects.push(person);
        person.name = '홍길동';
        person.description = '조선시대 의적';
        person.value = 30;  // 나이
        person.score = 95.5;  // 평가 점수

        console.log(`이름: ${person.name}`);
        console.log(`설명: ${person.description}`);
        console.log(`나이: ${person.value}`);
        console.log(`점수: ${person.score}`);
        console.log();

        // 예제 2: 전체 데이터로 생성
        console.log('='.repeat(50));
        console.log('예제 2: 전체 데이터로 생성');
        console.log('='.repeat(50));

        const product = new TestData(
            '노트북',
            '고성능 게이밍 노트북',
            1500000,  // 가격 (원)
            4.5  // 평점 (5점 만점)
        );
        allObjects.push(product);

        console.log(product.toString());
        console.log();

        // 예제 3: 객체 복사
        console.log('='.repeat(50));
        console.log('예제 3: 객체 복사');
        console.log('='.repeat(50));

        const productCopy = product.copy();
        allObjects.push(productCopy);
        console.log(`원본: ${product}`);
        console.log(`복사본: ${productCopy}`);
        console.log(`같은가?: ${product.isEqual(productCopy)}`);

        // 복사본 수정
        productCopy.name = '데스크톱';
        productCopy.value = 2000000;
        console.log(`\n수정된 복사본: ${productCopy}`);
        console.log(`이제 같은가?: ${product.isEqual(productCopy)}`);
        console.log();

        // 예제 4: 데이터 리스트 관리
        console.log('='.repeat(50));
        console.log('예제 4: 데이터 리스트 관리');
        console.log('='.repeat(50));

        // 학생 리스트
        const students = [];
        const studentData = [
            ['김철수', '컴퓨터공학과', 20, 92.5],
            ['이영희', '전자공학과', 21, 88.3],
            ['박민수', '기계공학과', 22, 95.7],
            ['정수진', '화학공학과', 20, 91.2],
        ];

        for (const [name, dept, age, score] of studentData) {
            const student = new TestData(name, dept, age, score);
            students.push(student);
            allObjects.push(student);
        }

        console.log('학생 명단:');
        students.forEach((student, i) => {
            const name = student.name.padEnd(10);
            const dept = student.description.padEnd(15);
            const age = String(student.value).padStart(3);
            const score = student.score.toFixed(1).padStart(5);
            console.log(`${i + 1}. ${name} - ${dept} 나이:${age} 점수:${score}`);
        });

        // 최고 점수 학생 찾기
        const bestStudent = students.reduce((max, student) => 
            student.score > max.score ? student : max
        );
        console.log(`\n최고 점수 학생: ${bestStudent.name} (${bestStudent.score}점)`);
        console.log();

        // 예제 5: JSON 변환 및 활용
        console.log('='.repeat(50));
        console.log('예제 5: JSON 변환 및 활용');
        console.log('='.repeat(50));

        const studentsJson = students.map(s => s.toJSON());
        console.log('학생 데이터를 JSON으로:');
        console.log(JSON.stringify(studentsJson, null, 2));
        console.log();

        // 예제 6: 데이터 초기화 및 재사용
        console.log('='.repeat(50));
        console.log('예제 6: 데이터 초기화 및 재사용');
        console.log('='.repeat(50));

        const temp = new TestData('임시', '임시 데이터', 999, 0.0);
        allObjects.push(temp);
        console.log(`초기화 전: ${temp}`);
        console.log(`비어있나?: ${temp.isEmpty()}`);

        temp.clear();
        console.log(`초기화 후: ${temp}`);
        console.log(`비어있나?: ${temp.isEmpty()}`);

        // 재사용
        temp.name = '재사용';
        temp.description = '재사용된 데이터';
        temp.value = 100;
        temp.score = 50.0;
        console.log(`재사용 후: ${temp}`);
        console.log();

        // 예제 7: C++ print 함수 사용
        console.log('='.repeat(50));
        console.log('예제 7: C++ print 함수 사용');
        console.log('='.repeat(50));
        console.log('C++ 측에서 출력:');
        person.print();
        console.log();

        // 예제 8: 함수형 프로그래밍 스타일
        console.log('='.repeat(50));
        console.log('예제 8: 함수형 프로그래밍 스타일');
        console.log('='.repeat(50));

        // 점수가 90점 이상인 학생들 필터링
        const excellentStudents = students.filter(s => s.score >= 90);
        console.log('우수 학생 (90점 이상):');
        excellentStudents.forEach(s => {
            console.log(`  ${s.name}: ${s.score}점`);
        });

        // 평균 점수 계산
        const avgScore = students.reduce((sum, s) => sum + s.score, 0) / students.length;
        console.log(`\n평균 점수: ${avgScore.toFixed(2)}점`);

        // 이름순 정렬
        const sortedByName = [...students].sort((a, b) => 
            a.name.localeCompare(b.name)
        );
        console.log('\n이름순 정렬:');
        sortedByName.forEach(s => console.log(`  ${s.name}`));
        console.log();

        console.log('='.repeat(50));
        console.log('모든 예제 완료!');
        console.log('='.repeat(50));

    } catch (error) {
        console.error(`오류: ${error.message}`);
        if (error.message.includes('찾을 수 없습니다')) {
            console.error('\n먼저 DLL을 빌드해야 합니다:');
            console.error('  Windows: build.bat 실행');
            console.error('  Linux:   ./build.sh 실행');
        } else {
            console.error(error.stack);
        }
    } finally {
        // 메모리 정리
        console.log('\n메모리 정리 중...');
        for (const obj of allObjects) {
            if (obj) {
                obj.destroy();
            }
        }
    }
}

// 실행
if (require.main === module) {
    main();
}

module.exports = { main };

