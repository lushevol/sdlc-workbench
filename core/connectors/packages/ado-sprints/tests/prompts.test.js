import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureSprintsPrompts } from '../src/prompts.js';

describe('Sprints Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('configureSprintsPrompts()', () => {
    it('should register 10 prompts on the server', () => {
      configureSprintsPrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(10);
    });

    it('should work without options argument', () => {
      expect(() => configureSprintsPrompts(mockServer)).not.toThrow();
    });

    it('should invoke default getContext when no options provided', async () => {
      configureSprintsPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sprint-planning');
      const result = await call.at(-1)({ project: 'P', team: 'T' });
      expect(result.messages[0].content.text).toBeDefined();
    });

    it('should accept optional getContext parameter', () => {
      const getContext = vi.fn(() => null);
      expect(() => configureSprintsPrompts(mockServer, { getContext })).not.toThrow();
    });

    it('should register all expected prompt names', () => {
      configureSprintsPrompts(mockServer);
      const names = mockServer.prompt.mock.calls.map(c => c[0]);
      expect(names).toContain('sprint-planning');
      expect(names).toContain('list-project-sprints');
      expect(names).toContain('create-sprints');
      expect(names).toContain('list-team-sprint-iterations');
      expect(names).toContain('assign-sprint-to-team');
      expect(names).toContain('get-sprint-capacities');
      expect(names).toContain('get-team-capacity');
      expect(names).toContain('update-team-capacity');
      expect(names).toContain('get-team-settings');
      expect(names).toContain('list-team-iterations');
    });
  });

  describe('sprint-planning prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sprint-planning');
      return call.at(-1)(args);
    };

    it('should return a user message with project and team', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam' });
      expect(result.messages[0].role).toBe('user');
      expect(result.messages[0].content.text).toContain('TBQPR');
      expect(result.messages[0].content.text).toContain('MyTeam');
    });

    it('should use context values when args not provided', async () => {
      const result = await invoke({}, { ado: { project: 'CtxProject', team: 'CtxTeam' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
      expect(result.messages[0].content.text).toContain('CtxTeam');
    });

    it('should show (required) placeholder when no project available', async () => {
      const result = await invoke({});
      expect(result.messages[0].content.text).toContain('(required)');
    });

    it('should handle null args gracefully', async () => {
      const result = await invoke(null);
      expect(result.messages[0].content.text).toBeDefined();
    });
  });

  describe('list-project-sprints prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'list-project-sprints');
      return call.at(-1)(args);
    };

    it('should include project in message', async () => {
      const result = await invoke({ project: 'TBQPR' });
      expect(result.messages[0].content.text).toContain('TBQPR');
    });

    it('should use context project when arg not provided', async () => {
      const result = await invoke({}, { ado: { project: 'CtxProject' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should show (required) placeholder when no project available', async () => {
      const result = await invoke({});
      expect(result.messages[0].content.text).toContain('(required)');
    });
  });

  describe('create-sprints prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-sprints');
      return call.at(-1)(args);
    };

    it('should include sprint name and project in message', async () => {
      const result = await invoke({ project: 'TBQPR', name: 'Sprint 42' });
      expect(result.messages[0].content.text).toContain('Sprint 42');
      expect(result.messages[0].content.text).toContain('TBQPR');
    });

    it('should include dates when provided', async () => {
      const result = await invoke({
        project: 'TBQPR',
        name: 'Sprint 42',
        startDate: '2026-06-01',
        endDate: '2026-06-14'
      });
      const text = result.messages[0].content.text;
      expect(text).toContain('2026-06-01');
      expect(text).toContain('2026-06-14');
    });

    it('should handle message without dates', async () => {
      const result = await invoke({ project: 'TBQPR', name: 'Sprint 42' });
      expect(result.messages[0].content.text).toContain('Sprint 42');
    });

    it('should use context project when arg not provided', async () => {
      const result = await invoke({ name: 'Sprint 1' }, { ado: { project: 'CtxProject' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should show (required) when no project available', async () => {
      const result = await invoke({ name: 'Sprint 42' });
      expect(result.messages[0].content.text).toContain('(required)');
    });
  });

  describe('list-team-sprint-iterations prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'list-team-sprint-iterations');
      return call.at(-1)(args);
    };

    it('should include project and team in message', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam' });
      expect(result.messages[0].content.text).toContain('TBQPR');
      expect(result.messages[0].content.text).toContain('MyTeam');
    });

    it('should include timeframe in message when provided', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam', timeframe: 'current' });
      expect(result.messages[0].content.text).toContain('current');
    });

    it('should handle message without timeframe', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam' });
      expect(result.messages[0].content.text).toContain('MyTeam');
    });

    it('should use context values when not provided in args', async () => {
      const result = await invoke({}, { ado: { project: 'CtxProject', team: 'CtxTeam' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should show (required) when no project or team available', async () => {
      const result = await invoke({});
      expect(result.messages[0].content.text).toContain('(required)');
    });
  });

  describe('assign-sprint-to-team prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'assign-sprint-to-team');
      return call.at(-1)(args);
    };

    it('should include project, team and iterationId in message', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam', iterationId: 'iter-guid-1' });
      const text = result.messages[0].content.text;
      expect(text).toContain('TBQPR');
      expect(text).toContain('MyTeam');
      expect(text).toContain('iter-guid-1');
    });

    it('should use context values when not provided', async () => {
      const result = await invoke({ iterationId: 'iter-1' }, { ado: { project: 'CtxProject', team: 'CtxTeam' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should show (required) when no project or team available', async () => {
      const result = await invoke({ iterationId: 'iter-1' });
      expect(result.messages[0].content.text).toContain('(required)');
    });
  });

  describe('get-sprint-capacities prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-sprint-capacities');
      return call.at(-1)(args);
    };

    it('should include project, team and iterationId in message', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam', iterationId: 'iter-guid-1' });
      const text = result.messages[0].content.text;
      expect(text).toContain('TBQPR');
      expect(text).toContain('MyTeam');
      expect(text).toContain('iter-guid-1');
    });

    it('should use context values when not provided', async () => {
      const result = await invoke({ iterationId: 'iter-1' }, { ado: { project: 'CtxProject', team: 'CtxTeam' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should show (required) when no project or team available', async () => {
      const result = await invoke({ iterationId: 'iter-1' });
      expect(result.messages[0].content.text).toContain('(required)');
    });
  });

  describe('get-team-capacity prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-team-capacity');
      return call.at(-1)(args);
    };

    it('should include project, team and iterationId in message', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam', iterationId: 'iter-guid-1' });
      const text = result.messages[0].content.text;
      expect(text).toContain('TBQPR');
      expect(text).toContain('MyTeam');
      expect(text).toContain('iter-guid-1');
    });

    it('should use context values when not provided', async () => {
      const result = await invoke({ iterationId: 'iter-1' }, { ado: { project: 'CtxProject', team: 'CtxTeam' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should show (required) when no project or team available', async () => {
      const result = await invoke({ iterationId: 'iter-1' });
      expect(result.messages[0].content.text).toContain('(required)');
    });
  });

  describe('update-team-capacity prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'update-team-capacity');
      return call.at(-1)(args);
    };

    it('should include all capacity update fields in message', async () => {
      const result = await invoke({
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1',
        teamMemberId: 'user-guid-1',
        activityName: 'Development',
        hoursPerDay: '6'
      });
      const text = result.messages[0].content.text;
      expect(text).toContain('TBQPR');
      expect(text).toContain('MyTeam');
      expect(text).toContain('Development');
      expect(text).toContain('6');
    });

    it('should use context values for project and team', async () => {
      const result = await invoke(
        { iterationId: 'iter-1', teamMemberId: 'user-1', activityName: 'Dev', hoursPerDay: '8' },
        { ado: { project: 'CtxProject', team: 'CtxTeam' } }
      );
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should show (required) when no project or team available', async () => {
      const result = await invoke(
        { iterationId: 'iter-1', teamMemberId: 'user-1', activityName: 'Dev', hoursPerDay: '8' }
      );
      expect(result.messages[0].content.text).toContain('(required)');
    });
  });

  describe('get-team-settings prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-team-settings');
      return call.at(-1)(args);
    };

    it('should include project in message', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam' });
      expect(result.messages[0].content.text).toContain('TBQPR');
      expect(result.messages[0].content.text).toContain('MyTeam');
    });

    it('should handle message without team parameter', async () => {
      const result = await invoke({ project: 'TBQPR' });
      expect(result.messages[0].content.text).toContain('TBQPR');
    });

    it('should use context project when not provided in args', async () => {
      const result = await invoke({}, { ado: { project: 'CtxProject' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should handle null args gracefully', async () => {
      const result = await invoke(null);
      expect(result.messages[0].content.text).toBeDefined();
    });
  });

  describe('list-team-iterations prompt message', () => {
    const invoke = async (args, ctx = null) => {
      configureSprintsPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'list-team-iterations');
      return call.at(-1)(args);
    };

    it('should include project and team in message', async () => {
      const result = await invoke({ project: 'TBQPR', team: 'MyTeam' });
      expect(result.messages[0].content.text).toContain('TBQPR');
      expect(result.messages[0].content.text).toContain('MyTeam');
    });

    it('should use context values when not provided in args', async () => {
      const result = await invoke({}, { ado: { project: 'CtxProject', team: 'CtxTeam' } });
      expect(result.messages[0].content.text).toContain('CtxProject');
      expect(result.messages[0].content.text).toContain('CtxTeam');
    });

    it('should handle null args gracefully', async () => {
      const result = await invoke(null);
      expect(result.messages[0].content.text).toBeDefined();
    });
  });
});
