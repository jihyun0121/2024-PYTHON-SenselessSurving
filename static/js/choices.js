import { stories } from './storys.js';

export function makeChoice(next, state, updateState, displayStory, selectNewStory, endGame, updateStatus) {
    switch (next) {
        case 'treasure':
            state.foundTreasures++;
            if (state.foundTreasures >= state.totalTreasures) {
                endGame('win');
            } else {
                selectNewStory();
                displayStory('start');
            }
            break;
        case 'fight_animal':
        case 'run_away':
        case 'escape_trap':
        case 'call_for_help':
            state.lives--;
            if (state.lives <= 0) {
                endGame('lose');
            } else {
                updateStatus();
                displayStory(next);
            }
            break;
        case 'gain_money':
            if (state.money < 3) {
                state.money++;
            }
            updateStatus();
            selectNewStory();
            displayStory('start');
            break;
        case 'lose_money':
            if (state.money > 0) {
                state.money--;
            }
            updateStatus();
            selectNewStory();
            displayStory('start');
            break;
        case 'gain_mental':
            if (state.mental < 3) {
                state.mental++;
            }
            updateStatus();
            selectNewStory();
            displayStory('start');
            break;
        case 'lose_mental':
            if (state.mental > 0) {
                state.mental--;
            }
            updateStatus();
            selectNewStory();
            displayStory('start');
            break;
        case 'inspect_relic':
            state.foundTreasures++;
            if (state.foundTreasures >= state.totalTreasures) {
                endGame('win');
            } else {
                selectNewStory();
                displayStory('start');
            }
            break;
        default:
            displayStory(next);
            break;
    }
}
