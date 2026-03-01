import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    console.log('Magic Skills extension is now active');

    // Register commands
    let listSkillsCmd = vscode.commands.registerCommand('magic-skills.listSkills', async () => {
        try {
            const config = vscode.workspace.getConfiguration('magicSkills');
            const apiEndpoint = config.get<string>('apiEndpoint') || 'http://localhost:3000';
            
            const response = await axios.get(`${apiEndpoint}/api/skills/list`);
            const skills = response.data;
            
            const items = skills.map((skill: any) => ({
                label: skill.name,
                description: skill.description,
                detail: `Category: ${skill.category}`
            }));
            
            const selected = await vscode.window.showQuickPick(items, {
                placeHolder: 'Select a skill to execute'
            });
            
            if (selected) {
                vscode.commands.executeCommand('magic-skills.executeSkill', selected.label);
            }
        } catch (error) {
            vscode.window.showErrorMessage('Failed to fetch skills. Is the Magic Skills server running?');
        }
    });

    let executeSkillCmd = vscode.commands.registerCommand('magic-skills.executeSkill', async (skillName?: string) => {
        if (!skillName) {
            skillName = await vscode.window.showInputBox({
                prompt: 'Enter skill name'
            });
        }
        
        if (!skillName) {
            return;
        }
        
        const params = await vscode.window.showInputBox({
            prompt: 'Enter parameters (JSON format)',
            value: '{}'
        });
        
        try {
            const config = vscode.workspace.getConfiguration('magicSkills');
            const apiEndpoint = config.get<string>('apiEndpoint') || 'http://localhost:3000';
            
            const response = await axios.post(`${apiEndpoint}/api/skills/execute`, {
                skill_name: skillName,
                params: JSON.parse(params || '{}')
            });
            
            const result = response.data;
            
            if (result.success) {
                const doc = await vscode.workspace.openTextDocument({
                    content: typeof result.data === 'string' ? result.data : JSON.stringify(result.data, null, 2),
                    language: 'text'
                });
                await vscode.window.showTextDocument(doc);
            } else {
                vscode.window.showErrorMessage(`Error: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage('Failed to execute skill. Is the Magic Skills server running?');
        }
    });

    let executeOnSelectionCmd = vscode.commands.registerCommand('magic-skills.executeOnSelection', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }
        
        const selection = editor.selection;
        const selectedText = editor.document.getText(selection);
        
        if (!selectedText) {
            vscode.window.showWarningMessage('No text selected');
            return;
        }
        
        const skillName = await vscode.window.showInputBox({
            prompt: 'Enter skill name to apply to selection'
        });
        
        if (!skillName) {
            return;
        }
        
        try {
            const config = vscode.workspace.getConfiguration('magicSkills');
            const apiEndpoint = config.get<string>('apiEndpoint') || 'http://localhost:3000';
            
            const response = await axios.post(`${apiEndpoint}/api/skills/execute`, {
                skill_name: skillName,
                params: { input: selectedText },
                context: {
                    file_path: editor.document.fileName,
                    language: editor.document.languageId
                }
            });
            
            const result = response.data;
            
            if (result.success) {
                const doc = await vscode.workspace.openTextDocument({
                    content: typeof result.data === 'string' ? result.data : JSON.stringify(result.data, null, 2),
                    language: editor.document.languageId
                });
                await vscode.window.showTextDocument(doc);
            } else {
                vscode.window.showErrorMessage(`Error: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage('Failed to execute skill. Is the Magic Skills server running?');
        }
    });

    context.subscriptions.push(listSkillsCmd, executeSkillCmd, executeOnSelectionCmd);
}

export function deactivate() {}
